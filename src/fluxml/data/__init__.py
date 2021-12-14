import os.path as osp
import gzip

from fluxml.config import DEFAULT
from fluxml import __name__ as NAME

from bpyutils.util.ml      import get_data_dir
from bpyutils.util.types   import build_fn
from bpyutils.util.system  import (
    get_files,
    make_temp_file
)
from bpyutils.util.string  import get_random_str
from bpyutils.util.types   import lmap
from bpyutils              import parallel, log

from bioservices import BiGG

import cobra

logger  = log.get_logger()

CSV_HEADER = []

def _download_bigg_model(model_id, data_dir = None):
    data_dir = get_data_dir(NAME, data_dir = data_dir)
    target   = osp.join(data_dir, "%s.xml.gz" % model_id)

    if not osp.exists(target):
        logger.info("Downloading BiGG Model %s..." % model_id)

        bigg = BiGG()
        bigg.download(model_id, format_ = "xml", target = target)
    else:
        logger.warn("BiGG Model %s already downloaded." % model_id)

def generate_flux_data(sbml_path, *args, **kwargs):
    data_dir = get_data_dir(NAME, kwargs.get("data_dir"))

    model    = None

    logger.info("Generating flux data for model at path: %s" % sbml_path)

    with gzip.open(sbml_path, "rb") as read_f:
        with make_temp_file() as tmp_file:
            with open(tmp_file, "wb") as write_f:
                content = read_f.read()
                write_f.write(content)

            model = cobra.io.read_sbml_model(tmp_file)

    if not model:
        raise ValueError("Unknown error while reading SBML file.")

    name       = model.name or get_random_str()
    output_csv = osp.join(data_dir, "%s.csv" % name)

    # if not osp.exists(output_csv):
    #     write(output_csv, ",".join(CSV_HEADER))

def generate_data(data_dir = None, check = False):
    data_dir = get_data_dir(NAME, data_dir = data_dir)
    # TODO: Generate Data
    files    = get_files(data_dir, "*.gz")

    if check:
        files = (osp.join(data_dir, "%s.xml.gz" % DEFAULT["bigg_model_id"]),)
    
    with parallel.no_daemon_pool() as pool:
        pool.lmap(generate_flux_data, files)

def get_data(data_dir = None, check = False, *args, **kwargs):
    data_dir = get_data_dir(NAME, data_dir)
    
    bigg   = BiGG()
    models = lmap(lambda x: x["bigg_id"], bigg.models)

    if check:
        models = (DEFAULT["bigg_model_id"],)
    
    with parallel.no_daemon_pool() as pool:
        function_ = build_fn(_download_bigg_model, data_dir = data_dir)
        pool.map(function_, models)

    generate_data(data_dir = data_dir, check = check)

def preprocess_data(data_dir = None, check = False, *args, **kwargs):
    data_dir = get_data_dir(data_dir)
    # do something ...