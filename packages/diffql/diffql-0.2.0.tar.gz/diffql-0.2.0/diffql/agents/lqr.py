import math
import numpy as np
import torch
import scipy.linalg
from diffql.agents.agents import AbstractAgent


class DLQR(AbstractAgent):
    def __init__(self, A, B, Q, R, gamma: float = 1.0):
        """
        DLQR stands for discrete-time linear quadratic regulator.

        For discounted DLQR, equations in [1] are modified.

        Dynamics and cost:
            Discrete time (DT) linear quadratic regulator (LQR).
            x[t+1] = A @ x[t] + B @ u[t]
            cost = sum_{t=0}^{\\infty} gamma**t x[t].T @ Q @ x[t] + u[t].T @ R @ u[t]
        Refs:
            [1] S. A. A. Rizvi and Z. Lin, “Output Feedback Q-Learning Control for the Discrete-Time Linear Quadratic Regulator Problem,” IEEE Trans. Neural Netw. Learning Syst., vol. 30, no. 5, pp. 1523–1536, May 2019, doi: 10.1109/TNNLS.2018.2870075.
            [2] https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.solve_discrete_are.html
            [3] https://en.wikipedia.org/wiki/Linear%E2%80%93quadratic_regulator#Infinite-horizon,_discrete-time_LQR
        """
        assert gamma > 0
        assert gamma <= 1.0
        self.gamma = gamma
        # first, solve the Ricatti equation [2]
        self.P = scipy.linalg.solve_discrete_are(math.sqrt(self.gamma)*A, B, Q, (1/self.gamma)*R)
        # Compute the LQR gain [3] and [1]
        self.K = scipy.linalg.inv((1/self.gamma)*R + B.T @ self.P @ B) @ (B.T @ self.P @ A)
        # for Q function [1, Eq. (12)] with modification for discounted LQR
        P_gamma = self.gamma * self.P
        self.H = np.block([
            [Q + A.T@P_gamma@A, A.T@P_gamma@B],
            [B.T@P_gamma@A, R + B.T@P_gamma@B],
        ])

    def forward(self, state, time=None):
        return -self.K @ state

    def Q_function(self, state, action):
        state_action = np.concatenate((state, action))
        z = state_action[:, None]  # reshape to be (n+m, 1)
        Q = (z.T @ self.H @ z).item()  # to make it float
        return Q
