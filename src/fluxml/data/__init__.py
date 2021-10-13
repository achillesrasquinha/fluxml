import os.path as osp
from functools import partial

from fluxml.config import PATH
from fluxml import __name__ as NAME

from bpyutils.util.environ import getenv
from bpyutils.util.system  import makedirs
from bpyutils.util.types   import lmap
from bpyutils              import parallel

from bioservices import BiGG

_PREFIX = NAME.upper()

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

def get_data(data_dir = None):
    data_dir = get_data_dir(data_dir)
    
    bigg   = BiGG()
    models = lmap(lambda x: x["bigg_id"], bigg.models)
    
    with parallel.no_daemon_pool() as pool:
        pool.map(
            partial(
                _download_bigg_model,
                **dict(data_dir = data_dir)
            )
        , models)

def preprocess_data(data_dir = None):
    data_dir = get_data_dir(data_dir)
    # do something ...