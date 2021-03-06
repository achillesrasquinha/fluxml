# imports - compatibility imports
from __future__ import absolute_import

# imports - standard imports
import os.path as osp
import traceback

from fluxml.commands.util 	    import cli_format
from bpyutils.util._dict        import merge_dict
from bpyutils.util.system   	import touch
from bpyutils.config			import environment
from bpyutils import log
from fluxml   import cli
from bpyutils._compat		    import iteritems
from fluxml.__attr__      	    import __name__ as NAME
from fluxml.exception           import DependencyNotFoundError

logger   = log.get_logger(name = NAME, level = log.DEBUG)

ARGUMENTS = dict(
    jobs						= 1,
    check		 				= False,
    interactive  				= False,
    yes			 				= False,
    no_cache		            = False,
    no_color 	 				= True,
    output						= None,
    ignore_error				= False,
    force						= False,
    verbose		 				= False
)

@cli.command
def command(**ARGUMENTS):
    try:
        return _command(**ARGUMENTS)
    except Exception as e:
        if not isinstance(e, DependencyNotFoundError):
            cli.echo()

            traceback_str = traceback.format_exc()
            cli.echo(traceback_str)

            cli.echo(cli_format("""\
An error occured while performing the above command. This could be an issue with
"fluxml". Kindly post an issue at https://github.com/achillesrasquinha/fluxml/issues""", cli.RED))
        else:
            raise e

def to_params(kwargs):
    class O(object):
        pass

    params = O()

    kwargs = merge_dict(ARGUMENTS, kwargs)

    for k, v in iteritems(kwargs):
        setattr(params, k, v)

    return params

def _command(*args, **kwargs):
    a = to_params(kwargs)

    if not a.verbose:
        logger.setLevel(log.NOTSET)

    logger.info("Environment: %s" % environment())
    logger.info("Arguments Passed: %s" % locals())

    file_ = a.output

    if file_:
        logger.info("Writing to output file %s..." % file_)
        touch(file_)
    
    logger.info("Using %s jobs..." % a.jobs)

    if a.fasta:
        fasta = osp.abspath(a.fasta)
        print(fasta)
        
        if not osp.exists(fasta):
            raise ValueError("No FASTA file found.")
        
        logger.info("Processing FASTA file %s..." % fasta)
        