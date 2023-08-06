import gym
from diffql.agents.agents import AbstractAgent


class ActionSampler(AbstractAgent):
    def __init__(self, action_space, seed=None):
        """
        action_space is defined from `gym`.
        """
        assert isinstance(action_space, gym.Space)
        self.action_space = action_space
        self.action_space.seed(seed)

    def forward(self, state, time=None):
        return self.action_space.sample()
