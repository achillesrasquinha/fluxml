# imports - standard imports
import subprocess as sp

class FluxmlError(Exception):
    pass

class PopenError(FluxmlError, sp.CalledProcessError):
    pass

class DependencyNotFoundError(ImportError):
    pass