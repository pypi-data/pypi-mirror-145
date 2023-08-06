import numpy as np

from diffql.agents.agents import AbstractAgent
from diffql.networks import AbstractParametrisedConvexApproximator


class ParametrisedConvexQAgent(AbstractAgent):
    def __init__(self, network, solver=None):
        assert isinstance(network, AbstractParametrisedConvexApproximator)
        self.network = network
        self.solver = solver  # default solver

    def forward(self, state, time=None, solver=None):
        if solver is None:
            solver = self.solver
        action = self.network.minimise_np(state, solver=solver)
        return action
