import numpy as np

from bpyutils._compat import iteritems

def create_sparse_stoichiometric_matrix(model, dtype = np.float64):
    metabolites   = model.metabolites
    reactions     = model.reactions

    n_metabolites = len(metabolites)
    n_reactions   = len(reactions)

    matrix        = np.zeros((n_metabolites, n_reactions * 2), dtype = dtype) # account for reversible reactions too.

    m_index       = metabolites.index
    r_index       = reactions.index

    for reaction in model.reactions:
        for metabolite, coeff in iteritems(reaction.metabolites):
            matrix[m_index(metabolite), r_index(reaction)]      = coeff

            coeff = -coeff if reaction.reversibility else 0

            matrix[m_index(metabolite), r_index(reaction) + 1]  = coeff

    return matrix