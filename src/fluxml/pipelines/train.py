from bpyutils.util.ml import get_data_dir

from fluxml import __name__

NAME = __name__.upper()

def build_model():
    pass
    # do something ...

def train(data_dir = None, artifacts_dir = None, *args, **kwargs):
    data_dir = get_data_dir(NAME, data_dir = data_dir)
    model    = build_model()
    # do something ...