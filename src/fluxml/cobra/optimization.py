import numpy as np

from pymoo.core.problem import Problem as PyMOOProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize

from bpyutils._compat import iteritems

ALGORITHMS = {
    "nsga2": {
        "class": NSGA2
    }
}

def _get_bounds(model, type_):
    attr    = "%s_bound" % type_
    bounds  = []

    for reaction in model.reactions:
        bound = getattr(reaction, attr)
        bounds += [bound, bound]

    return bounds

def _get_obj_coeff_arr(model):
    reactions   = model.reactions
    n_reactions = len(reactions)

    matrix      = np.zeros((n_reactions * 2, 1))

    r_index     = reactions.index

    for _, objective in iteritems(model.objectives):
        for variable in objective.variables:
            name = variable.name

            if "reverse" not in name:
                reaction = reactions.get_by_id(name)

                matrix[r_index(reaction), 0]     = 1
                matrix[r_index(reaction) + 1, 0] = -1

    return matrix

class OptimizationProblem(PyMOOProblem):
    def __init__(self, *args, **kwargs):
        model       = kwargs["model"]

        self._super = super(OptimizationProblem, self)
        self._super.__init__(
            n_var       = len(model.variables),
            n_constr    = len(model.constraints),
            n_obj       = len(model.objectives),
            xl          = _get_bounds(model, "lower"),
            xb          = _get_bounds(model, "upper")
        , *args, **kwargs)

        self._model     = model

    @property
    def model(self):
        return self._model

    def _evaluate(self, x, out, *args, **kwargs):
        model    = self.model
        X        = np.transpose(x)

        coeff    = _get_obj_coeff_arr(model)
        S        = model.sparse_stoichiometric_matrix

        out["F"] = np.dot(np.transpose(coeff), X)
        out["G"] = np.dot(S, X)

class Problem:
    def __init__(self, model):
        self._model = model

    @property
    def model(self):
        return self._model

    def solve(self, *args, **kwargs):
        model     = self.model

        algorithm = kwargs.get("algorithm", "nsga2")

        if algorithm not in ALGORITHMS:
            raise ValueError("Algorithm %s not found." % algorithm)

        algorithm_class     = ALGORITHMS[algorithm]["class"]
        algorithm_instance  = algorithm_class()

        problem = OptimizationProblem(model = model)

        result  = minimize(problem, algorithm_instance)

        return result