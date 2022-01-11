import numpy as np

from pymoo.core.problem import Problem as PyMOOProblem

class Problem(PyMOOProblem):
    def __init__(self, *args, **kwargs):
        constraints = kwargs.pop("constraints", {})
        
        self._super = super(Problem, self)
        self._super.__init__(n_constr = len(constraints), *args, **kwargs)

        self._constraints = constraints

    @property
    def constraints(self):
        return self._constraints

    def _evaluate(self, x, out, *args, **kwargs):
        for constraint in self.constraints:
            print(constraint)

        out["G"] = None