import os.path as osp
from functools import partial
import gzip

from fluxml.config import PATH
from fluxml import __name__ as NAME

from bpyutils.util.environ import getenv
from bpyutils.util.system  import (
    makedirs,
    get_files,
    make_temp_file
)
from bpyutils.util.types   import lmap
from bpyutils              import parallel, log

from bioservices import BiGG

import cobra
from   memote.support.helpers import find_transport_reactions

_PREFIX = NAME.upper()

DEFAULT_BIGG_MODEL_ID = "e_coli_core"

logger = log.get_logger()

def get_data_dir(data_dir = None):
    data_dir = data_dir \
        or getenv("DATA_DIR", prefix = _PREFIX) \
        or osp.join(PATH["CACHE"], "data")

    makedirs(data_dir, exist_ok = True)

    return data_dir

def _download_bigg_model(model_id, data_dir = None):
    data_dir = get_data_dir(data_dir = data_dir)
    target   = osp.join(data_dir, "%s.xml.gz" % model_id)

    bigg     = BiGG()
    bigg.download(model_id, format_='xml', target = target)

def _prune_model(model):
    rxn_exchange  = model.exchanges
    rxn_transport = list(find_transport_reactions(model))
    
    prune_rxns    = rxn_exchange; # + rxn_transport

    for rxn in prune_rxns:
        rxn.remove_from_model(remove_orphans = True)

def _generate_flux_data(sbml_path, data_dir = None):
    model = None

    with gzip.open(sbml_path, "rb") as read_f:
        with make_temp_file() as tmp_file:
            with open(tmp_file, "wb") as write_f:
                content = read_f.read()
                write_f.write(content)

            model = cobra.io.read_sbml_model(tmp_file)

    if not model:
        raise ValueError("Unknown error while reading SBML file.")
    
    # _prune_model(model)

def generate_data(data_dir = None, check = False):
    data_dir = get_data_dir(data_dir)
    # TODO: Generate Data

    files    = get_files(data_dir, "*.gz")

    if check:
        files = (osp.join(data_dir, "%s.xml.gz" % DEFAULT_BIGG_MODEL_ID),)
    
    with parallel.no_daemon_pool() as pool:
        pool.lmap(_generate_flux_data, files)

def get_data(data_dir = None, check = False, *args, **kwargs):
    data_dir = get_data_dir(data_dir)
    
    bigg   = BiGG()
    models = lmap(lambda x: x["bigg_id"], bigg.models)

    if check:
        models = (DEFAULT_BIGG_MODEL_ID,)
    
    with parallel.no_daemon_pool() as pool:
        pool.map(
            partial(
                _download_bigg_model,
                **dict(data_dir = data_dir)
            )
        , models)

    generate_data(data_dir = data_dir, check = check)

def preprocess_data(data_dir = None, check = False, *args, **kwargs):
    data_dir = get_data_dir(data_dir)
    # do something ...