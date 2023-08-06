from math import isclose
import numpy as np
from gym import spaces

from diffql.envs.envs import AbstractEnv
from diffql.envs.envs import LinearQuadraticDTEnv


class SimpleEnv(LinearQuadraticDTEnv):
    observation_space_shape = (1,)
    action_space_shape = (1,)
    # plant matirx
    A = np.array([
        [1.0],
    ])
    # control matirx
    B = np.array([
        [1.0],
    ])

    def __init__(
        self, initial_state=np.zeros(observation_space_shape), dt=1.0, max_t=10.0,
        Q=np.eye(observation_space_shape[0]), R=np.eye(action_space_shape[0]),
        x_min=None, x_max=None, u_min=None, u_max=None,
    ):
        super().__init__(initial_state, self.A, self.B, Q, R, max_t, dt, x_min, x_max, u_min, u_max)


class MechanicalDTEnv(LinearQuadraticDTEnv):
    """
    [1, Section IV.A]
    [1] G. C. Calafiore and C. Possieri, “Efficient Model-Free Q-Factor Approximation in Value Space via Log-Sum-Exp Neural Networks,” in 2020 European Control Conference (ECC), Saint Petersburg, Russia, May 2020, pp. 23–28. doi: 10.23919/ECC51009.2020.9143765.
    """
    observation_space_shape = (4,)
    action_space_shape = (1,)
    # plant matirx
    A = np.array([
        [0.0289, 0.0010, 0.0475, 0.0019],
        [-3.0836, 0.0226, -6.4323, 0.0442],
        [0.0379, 0.0013, 0.0621, 0.0026],
        [-4.1300, 0.0295, -8.6020, 0.0578],
    ])
    # control matirx
    B = np.array([
        [0],
        [0],
        [0],
        [6.6667],
    ])

    def __init__(
        self, initial_state=np.zeros(observation_space_shape), dt=1, max_t=11,
        Q=np.eye(observation_space_shape[0]), R=np.eye(action_space_shape[0]),
        x_min=None, x_max=None, u_min=None, u_max=None,
    ):
        super().__init__(initial_state, self.A, self.B, Q, R, max_t, dt, x_min, x_max, u_min, u_max)


class TwoDimensionalLinearDTSystem(AbstractEnv):
    """
    See https://github.com/JinraeKim/diffql/issues/34 for details.
    """
    observation_space_shape = (2,)
    action_space_shape = (1,)

    def __init__(
            self, initial_state=np.zeros(observation_space_shape), c=0.75, d=1, dt=1.0, max_t=20.0,
            x_min=None, x_max=None, u_min=None, u_max=None):
        super().__init__(max_t=max_t, dt=dt)

        if x_min is None:
            x_min = -np.inf * np.ones(self.observation_space_shape[0])
        if x_max is None:
            x_max = np.inf * np.ones(self.observation_space_shape[0])
        if u_min is None:
            u_min = -np.inf * np.ones(self.action_space_shape[0])
        if u_max is None:
            u_max = np.inf * np.ones(self.action_space_shape[0])
        self.observation_space = spaces.Box(low=x_min, high=x_max, dtype=np.float64)
        self.action_space = spaces.Box(low=u_min, high=u_max, dtype=np.float64)

        assert c > 0.0 and c < 1.0, "Constant c must be within (0, 1)"
        self.c = c
        self.A = np.array([
            [self.c, self.c],
            [0.0, self.c]
        ])
        self.B = np.array([
            [0.0],
            [1.0]
        ])
        assert d > 0.0, "Constant d must be greater than zero"
        self.d = d
        self.initial_state = initial_state
        self.state = initial_state

    def dynamics(self, state, action, time=None):
        x = state[:, None]  # reshape to be (n, 1)
        u = action[:, None]  # reshape to be (m, 1)
        x_next = self.A @ x + self.B @ u
        next_state = x_next.reshape(state.shape)
        return next_state

    def reward_function(self, state, action):
        x1, x2 = state
        u = action[0]
        a = self.minus_cubic_solution(x2)
        r_bar = (
            (3/4) * a**4
            + a**2
            - self.d * self.V1(self.c * x1 + self.c * x2)
            + (1 - self.c**2) * x2**2
            + self.d * self.V1(x1)
        )
        cost = r_bar + (1/4) * u**4
        return -cost

    def V1(self, x1):
        if x1 > 0.0:
            out = x1**(1/4)  # concave
        else:
            out = x1**4  # convex
        return out

    def value(self, state):
        x1, x2 = state
        return self.d * self.V1(x1) + x2**2

    def Q_value(self, state, action):
        r = self.reward_function(state, action)
        next_state = self.dynamics(state, action)
        return r + self.value(next_state)

    def optimal_control(self, state):
        x2 = state[1]
        a = self.minus_cubic_solution(x2)
        return np.array([-a])

    def step(self, action):
        state = self.state
        reward = self.reward_function(state, action)

        done_dict = self.get_done_dict(state)
        next_state = self.propagate(state, action)
        self.state = next_state
        is_bellman_equation_satisfied = self.check_bellman_equation_is_satisfied(state, action, next_state)
        info = {
            "done_dict": done_dict,
            "optimality_condition": is_bellman_equation_satisfied,
        }  # append some info if necessary
        return next_state, reward, any(done_dict.values()), info

    def reset(self, seed=None):
        super().reset(seed=seed)  # clock, etc.
        self.state = self.initial_state
        return self.state

    def check_bellman_equation_is_satisfied(self, state, action, next_state):
        reward = self.reward_function(state, action)
        next_value = self.value(next_state)
        value = self.value(state)
        bellman_equation = reward + next_value - value  # >= 0, =0 for optimal control
        return isclose(bellman_equation, 0.0, abs_tol=1e-8)

    def minus_cubic_solution(self, x2: float) -> float:
        a = 1.0
        b = 0.0
        c = 2.0
        d = 2 * self.c * x2
        roots = np.poly1d([a, b, c, d]).r
        # there exist exactly one real root u = -a;
        # we can find real root by comparing magnitudes of imaginary part of roots
        idx = np.argmin(abs(roots.imag))
        real_root = roots[idx].real
        assert isclose(a * real_root**3 + b * real_root**2 + c * real_root + d, 0, abs_tol=1e-10), 'This value does not satisfy the cubic equation'
        # solution u = -a to u^3 + 2u + 2cx2 = (u+a)(u^2 -au + 2+a^2) = 0
        # Note: why -real_root? => a is defined as the unique real solution to the equation of this form: (u+a)(u^2 - au + (2+a^2)) = 0
        return -real_root
