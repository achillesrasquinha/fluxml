import os.path as osp
import gzip
import random

from fluxml import __name__ as NAME

from bpyutils.util.ml      import get_data_dir
from bpyutils.util.system  import (
    make_temp_file
)
from bpyutils.util.array   import flatten
from bpyutils.util.types   import lmap, build_fn
from bpyutils.util.string  import get_random_str
from bpyutils.util._csv    import write as write_csv
from bpyutils              import log, parallel

import cobra
import optlang

from fluxml import settings

logger = log.get_logger()

CSV_HEADER_PRE  = []
CSV_HEADER_POST = ["objective_value"]

MINIMUM_LOWER_BOUND = -1000
MAXIMUM_UPPER_BOUND =  1000

def optimize_model_and_save(model, output, **kwargs):
    solution  = model.optimize()

    if solution.status != optlang.interface.INFEASIBLE:
        objective_value = solution.objective_value

        row = []

        for reaction in model.reactions:
            row += reaction.bounds

        row.append(objective_value)

        write_csv(output, row, mode = "a+")

def knock_out_random_genes(model, output):
    logger.info("Using strategy: knock_out_random_genes...")

    while True:
        genes     = model.genes
        ngenes    = len(genes)

        nknockout = random.randint(1, ngenes)

        with model:
            knockout_genes = random.sample(genes, nknockout)
            for gene in knockout_genes:
                gene.knock_out()

            logger.info("Knocked Out %s genes." % nknockout)

            optimize_model_and_save(model, output)

def knock_out_random_reactions(model, output):
    logger.info("Using strategy: knock_out_random_reactions...")

    while True:
        reactions  = model.reactions
        nreactions = len(reactions)

        nknockout  = random.randint(1, nreactions)

        with model:
            knockout_reactions = random.sample(reactions, nknockout)
            for reaction in knockout_reactions:
                reaction.knock_out()

            logger.info("Knocked Out %s reactions." % nknockout)

            optimize_model_and_save(model, output)

def randomize_reaction_bounds(model, output):
    logger.info("Using strategy: randomize_reaction_bounds...")

    while True:
        reactions  = model.reactions
        nreactions = len(reactions)

        nrandom    = random.randint(1, nreactions)

        with model:
            for _ in range(nrandom):
                reaction = random.choice(reactions)

                reaction.lower_bound = random.uniform(MINIMUM_LOWER_BOUND, 0)
                reaction.upper_bound = random.uniform(0, MAXIMUM_UPPER_BOUND)

            logger.info("Randomized %s reaction bounds." % nrandom)

            optimize_model_and_save(model, output)

def mutate_model_and_save(strategy, model, output):
    strategy(model, output)

def generate_flux_data(sbml_path, **kwargs):
    jobs = kwargs.get("jobs", settings.get("jobs"))
    data_dir = get_data_dir(NAME, kwargs.get("data_dir"))

    model    = None

    logger.info("Generating flux data for model at path: %s" % sbml_path)

    with gzip.open(sbml_path, "rb") as read_f:
        with make_temp_file() as tmp_file:
            with open(tmp_file, "wb") as write_f:
                content = read_f.read()
                write_f.write(content)

            model       = cobra.io.read_sbml_model(tmp_file)

            name        = model.id or model.name or get_random_str()
            output_csv  = osp.join(data_dir, "%s.csv" % name)

            reactions   = model.reactions

            if not osp.exists(output_csv):
                reaction_bounds_columns = flatten(
                    lmap(lambda x: ("%s_lb" % x.id, "%s_ub" % x.id), reactions)
                )
                header = CSV_HEADER_PRE + reaction_bounds_columns + CSV_HEADER_POST
                write_csv(output_csv, header)

            strategies  = [
                knock_out_random_genes,
                knock_out_random_reactions,
                randomize_reaction_bounds
            ]

            with parallel.no_daemon_pool(processes = jobs) as pool:
                function = build_fn(mutate_model_and_save, model = model, output = output_csv)
                list(pool.map(function, strategies))