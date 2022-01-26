from cobra.core.model import Model as COBRAPyModel

from bpyutils._compat import iteritems

from fluxml.cobra.optimization import Problem
from fluxml.cobra.util import create_sparse_stoichiometric_matrix

class Model(COBRAPyModel):
    def __init__(self, *args, **kwargs):
        self._super = super(Model, self)
        self._super.__init__(*args, **kwargs)

        self._objectives = []

    @property
    def objectives(self):
        objectives = {}

        if self.objective:
            objective = self.objective

            objectives[objective.name] = objective

        return objectives

    @property
    def sparse_stoichiometric_matrix(self):
        return create_sparse_stoichiometric_matrix(self)

    def optimize(self, *args, **kwargs):
        algorithm = kwargs.get("algorithm", "nsga2")

        problem   = Problem(self)

        solution  = problem.solve(algorithm = algorithm)

        solution  = self._super.optimize(*args, **kwargs)
        return solution