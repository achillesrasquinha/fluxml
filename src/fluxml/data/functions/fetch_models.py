import os.path as osp

from fluxml.config import DEFAULT
from fluxml import __name__ as NAME

from bpyutils.util.ml      import get_data_dir
from bpyutils.util.types   import build_fn
from bpyutils.util.types   import lmap
from bpyutils              import parallel, log

from bioservices import BiGG

logger = log.get_logger()

def download_bigg_model(model_id, data_dir = None):
    data_dir = get_data_dir(NAME, data_dir = data_dir)
    target   = osp.join(data_dir, "%s.xml.gz" % model_id)

    if not osp.exists(target):
        logger.info("Downloading BiGG Model %s..." % model_id)

        bigg = BiGG()
        bigg.download(model_id, format_ = "xml", target = target)
    else:
        logger.warn("BiGG Model %s already downloaded." % model_id)

def fetch_bigg_models(data_dir = None, check = False, *args, **kwargs):
    bigg = BiGG()
    model_ids = lmap(lambda x: x["bigg_id"], bigg.models)

    if check:
        model_ids = (DEFAULT["bigg_model_id"],)
    
    with parallel.no_daemon_pool() as pool:
        function_ = build_fn(download_bigg_model, data_dir = data_dir)
        pool.map(function_, model_ids)

def fetch_models(data_dir = None, check = False, *args, **kwargs):
    fetch_bigg_models(data_dir = data_dir, check = check, *args, **kwargs)