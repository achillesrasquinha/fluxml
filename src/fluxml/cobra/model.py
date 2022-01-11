from cobra.core.model import Model as COBRAPyModel

from bpyutils._compat import iteritems

from fluxml.cobra.problem import Problem

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

    def optimize(self, *args, **kwargs):
        def get_bounds(type_):
            attr    = "%s_bound" % type_
            bounds  = []

            for reaction in self.reactions:
                bound = getattr(reaction, attr)
                bounds += [bound, bound]

            return bounds

        for key, item in iteritems(self.constraints):
            pass

        problem  = Problem(
            n_var       = len(self.variables),
            n_obj       = len(self.objectives),
            xl          = get_bounds("lower"),
            xu          = get_bounds("upper"),

            constraints = self.constraints,
        )

        solution = self._super.optimize(*args, **kwargs)
        return solution