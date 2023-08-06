import logging

import argparse

import sys

from typing import List


from JuMonC import settings
from JuMonC import reset_logging


logger = logging.getLogger(__name__)



def parseCMDOptions(args: List[str] = None) -> None:
    if args is None:
        args = []

    parser = setupParser()
    checkParserArgs(parser, args)

    

def setupParser() -> argparse.ArgumentParser:
    #pylint: disable=import-outside-toplevel
    from JuMonC._version import __REST_version__, REST_version_info, __version__
    #pylint: enable=import-outside-toplevel

    parser = argparse.ArgumentParser(description=("JuMonC is the Jülich Monitoring and Control programm, "
                                                  "it allows to monitore your running simulations and access avaiable data using a REST-API"),
                                     prog="app.py",)

    parser.add_argument("--DONT_DEFAULT_TO_HUMAN_READABLE_NUMBERS", 
                       dest="DONT_DEFAULT_TO_HUMAN_READABLE_NUMBERS", 
                       help="Sets wether numbers are converted into smaller numbers by default, can be overwritten for each API call", 
                       default=True, 
                       action='store_false')
    parser.add_argument("--LOG_FORMAT", 
                       dest="LOG_FORMAT", 
                       help="Set log format, usable values are the values supported by logging", 
                       default="[%(asctime)s][PID:%(process)d][%(levelname)s][%(name)s] %(message)s", type=ascii)
    parser.add_argument("--LOG_LEVEL", 
                       dest="LOG_LEVEL", 
                       help="Set the log level used by the logger", 
                       default="INFO", 
                       type=ascii, 
                       choices=["'ERROR'", "'WARN'", "'INFO'", "'DEBUG'"])
    parser.add_argument("--LOG_STDOUT", 
                       dest="LOG_STDOUT", 
                       help="If used log to stdout, otherwise to stderr", 
                       default=False, 
                       action='store_true')
    parser.add_argument("--LOG_PREFIX", 
                       dest="LOG_PREFIX", 
                       help="Set a prefix that will be prefaced to every logging output", 
                       default="", 
                       type=ascii)
    parser.add_argument("--MAX_WORKER_THREADS", 
                       dest="MAX_WORKER_THREADS", 
                       help="Limits the number of worker threads that work on the actual tasks at once", 
                       default=4, 
                       type=int)
    parser.add_argument("--ONLY_CHOOSEN_REST_API_VERSION", 
                       dest="ONLY_CHOOSEN_REST_API_VERSION", 
                       help="If set will only provide one version of the api links", 
                       default=False, 
                       action='store_true')
    parser.add_argument("--PENDING_TASKS_SOFT_LIMIT", 
                       dest="PENDING_TASKS_SOFT_LIMIT", 
                       help="Limits tasks being added by the REST-API, to not have more than PENDING_TASKS_SOFT_LIMIT tasks waiting", 
                       default=100, 
                       type=int)
    parser.add_argument("-p", "--REST_API_PORT", 
                       dest="REST_API_PORT", 
                       help="Choose a port that the REST-API will be listening on", 
                       default=12121, 
                       type=int, 
                       metavar="[1024-65535]")
    parser.add_argument("--REST_API_VERSION", 
                       dest="REST_API_VERSION", 
                       help=("Choose a major version of the rest api. Depending on ONLY_CHOOSEN_REST_API_VERSION, "
                       "only this version, or all versions up to this version will be avaiable"), 
                       default=REST_version_info[0], 
                       choices=range(REST_version_info[0]+1), 
                       type=int)
    parser.add_argument("--SHORT_JOB_MAX_TIME", 
                       dest="SHORT_JOB_MAX_TIME", 
                       help=("Short jobs will be executed rigth away and return results directly via REST-API, "
                       "blocking all other mpi communication in between [s]"), 
                       default=0.1, 
                       type=float)
    parser.add_argument("--USER_DEFINED_TOKEN", 
                       dest="USER_DEFINED_TOKEN", 
                       help=("Define one additional token with scope level, separate multiple tokens by ;"
                       "Example \"--USER_DEFINED_TOKEN=12345678:100\""), 
                       default=None, 
                       type=str)
    parser.add_argument("-v", 
                       "--version", 
                       help="Print Version number of JuMonC", 
                       action='version', 
                       version=f'JuMonC\'s {__version__}, REST-API\'s {__REST_version__}')
    
    return parser


def checkParserArgs(parser: argparse.ArgumentParser, args: List[str]) -> None:
    #pylint: disable=import-outside-toplevel
    from JuMonC._version import REST_version_info
    #pylint: enable=import-outside-toplevel
    
    parsed = parser.parse_args(args)
          
    #set new logging options first, to then use them
    LOG_LEVEL = parsed.LOG_LEVEL[1:-1]
    if settings.LOG_LEVEL != LOG_LEVEL:
        settings.LOG_LEVEL = LOG_LEVEL
        logging.warning("Changing LOG_LEVEL to %s", settings.LOG_LEVEL)
        reset_logging()
    
    if settings.LOG_STDOUT != parsed.LOG_STDOUT:
        settings.LOG_STDOUT = parsed.LOG_STDOUT
        logging.warning("Changing LOG_STDOUT to %s", str(settings.LOG_STDOUT))
        reset_logging()
    
    LOG_PREFIX = parsed.LOG_PREFIX[1:-1]
    if settings.LOG_PREFIX != LOG_PREFIX:
        settings.LOG_PREFIX = LOG_PREFIX
        logging.warning("Changing LOG_PREFIX to %s", settings.LOG_PREFIX)
        reset_logging()
    
    LOG_FORMAT = parsed.LOG_FORMAT[1:-1]
    if settings.LOG_FORMAT != LOG_FORMAT:
        settings.LOG_FORMAT = LOG_FORMAT
        logging.warning("Changing LOG_FORMAT to %s", settings.LOG_FORMAT)
        reset_logging()
    
    
    
    settings.DEFAULT_TO_HUMAN_READABLE_NUMBERS = parsed.DONT_DEFAULT_TO_HUMAN_READABLE_NUMBERS
    logging.info("Set DEFAULT_TO_HUMAN_READABLE_NUMBERS to %s", str(settings.DEFAULT_TO_HUMAN_READABLE_NUMBERS))

        
    if parsed.MAX_WORKER_THREADS >= 1:
        settings.MAX_WORKER_THREADS = parsed.MAX_WORKER_THREADS
        logging.info("Set MAX_WORKER_THREADS to %s", str(settings.MAX_WORKER_THREADS))
    else:
        settings.MAX_WORKER_THREADS = 1
        logging.warning("Invalid value for MAX_WORKER_THREADS: %s%s%s%s",
                        str(parsed.MAX_WORKER_THREADS), 
                        ", needs to be at valid version! Set to ",
                        str(settings.MAX_WORKER_THREADS ),
                        " now.")


    settings.ONLY_CHOOSEN_REST_API_VERSION = parsed.ONLY_CHOOSEN_REST_API_VERSION
    logging.info("Set ONLY_CHOOSEN_REST_API_VERSION to %s", str(settings.ONLY_CHOOSEN_REST_API_VERSION))


    if parsed.PENDING_TASKS_SOFT_LIMIT >= 1:
        settings.PENDING_TASKS_SOFT_LIMIT = parsed.PENDING_TASKS_SOFT_LIMIT
        logging.info("Set PENDING_TASKS_SOFT_LIMIT to %s", str(settings.PENDING_TASKS_SOFT_LIMIT))
    else:
        settings.PENDING_TASKS_SOFT_LIMIT = 1
        logging.warning("Invalid value for PENDING_TASKS_SOFT_LIMIT: %s%s%s%s",
                        str(parsed.PENDING_TASKS_SOFT_LIMIT), 
                        ", needs to be at valid version! Set to ",
                        str(settings.PENDING_TASKS_SOFT_LIMIT ),
                        " now.")


    if parsed.REST_API_PORT >=1024 and parsed.REST_API_PORT<=65535:
        settings.REST_API_PORT = parsed.REST_API_PORT
        logging.info("Set REST_API_PORT to %s", str(settings.REST_API_PORT))
    else:
        logging.error("Invalid value for REST_API_PORT: %s%s", str(settings.REST_API_PORT), ", needs to be between 1024 and 65535")
        sys.exit(-1)

        
    if parsed.REST_API_VERSION >= 1 and parsed.REST_API_VERSION <= REST_version_info[0]:
        settings.REST_API_VERSION = parsed.REST_API_VERSION
        logging.info("Set REST_API_VERSION to %s", str(settings.REST_API_VERSION))
    else:
        settings.REST_API_VERSION = REST_version_info[0]
        logging.warning("Invalid value for REST_API_VERSION: %s%s%s%s",
                        str(parsed.REST_API_VERSION), 
                        ", needs to be at least 1! Set to ",
                        str(settings.REST_API_VERSION ),
                        " now.")


    settings.SHORT_JOB_MAX_TIME = parsed.SHORT_JOB_MAX_TIME
    logging.info("Set SHORT_JOB_MAX_TIME to %s", str(settings.SHORT_JOB_MAX_TIME))
    
    
    settings.USER_DEFINED_TOKEN = parsed.USER_DEFINED_TOKEN
    logging.info("Set USER_DEFINED_TOKEN to %s", str(settings.USER_DEFINED_TOKEN))
