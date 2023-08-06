from JuMonC.helpers import cmdArguments
from JuMonC._version import __REST_version__, REST_version_info, __version__
from JuMonC import settings


def test_Log_Format_setting():
    cmdArguments.parseCMDOptions(["--LOG_FORMAT", "[%(asctime)s]"])
    assert( settings.LOG_FORMAT == "[%(asctime)s]")
    
    # default:
    cmdArguments.parseCMDOptions([])
    assert( settings.LOG_FORMAT == "[%(asctime)s][PID:%(process)d][%(levelname)s][%(name)s] %(message)s")

    
def test_Log_Level_setting():
    cmdArguments.parseCMDOptions(["--LOG_LEVEL", "ERROR"])
    assert( settings.LOG_LEVEL == "ERROR")
    
    cmdArguments.parseCMDOptions(["--LOG_LEVEL", "WARN"])
    assert( settings.LOG_LEVEL == "WARN")
    
    cmdArguments.parseCMDOptions(["--LOG_LEVEL", "INFO"])
    assert( settings.LOG_LEVEL == "INFO")
    
    cmdArguments.parseCMDOptions(["--LOG_LEVEL", "DEBUG"])
    assert( settings.LOG_LEVEL == "DEBUG")
    
    # default:
    cmdArguments.parseCMDOptions([])
    assert( settings.LOG_LEVEL == "INFO")
    
    # different argument style
    cmdArguments.parseCMDOptions(["--LOG_LEVEL=DEBUG"])
    assert( settings.LOG_LEVEL == "DEBUG")

    
def test_Log_Stdout_setting():
    cmdArguments.parseCMDOptions(["--LOG_STDOUT"])
    assert( settings.LOG_STDOUT == True)
    
    # default:
    cmdArguments.parseCMDOptions([])
    assert( settings.LOG_STDOUT == False)


def test_Log_Prefix_setting():
    cmdArguments.parseCMDOptions(["--LOG_PREFIX", "[test]"])
    assert( settings.LOG_PREFIX == "[test]")
    
    # default:
    cmdArguments.parseCMDOptions([])
    assert( settings.LOG_PREFIX == "")


def test_MAX_WORKER_THREADS_setting():
    cmdArguments.parseCMDOptions(["--MAX_WORKER_THREADS", "35"])
    assert( settings.MAX_WORKER_THREADS == 35)
    
    # invalid value
    cmdArguments.parseCMDOptions(["--MAX_WORKER_THREADS", "-35"])
    assert( settings.MAX_WORKER_THREADS == 1)
    
    # default:
    cmdArguments.parseCMDOptions([])
    assert( settings.MAX_WORKER_THREADS == 4)

    
def test_ONLY_CHOOSEN_REST_API_VERSION_setting():
    cmdArguments.parseCMDOptions(["--ONLY_CHOOSEN_REST_API_VERSION"])
    assert( settings.ONLY_CHOOSEN_REST_API_VERSION == True)
    
    # default:
    cmdArguments.parseCMDOptions([])
    assert( settings.ONLY_CHOOSEN_REST_API_VERSION == False)


def test_PENDING_TASKS_SOFT_LIMIT_setting():
    cmdArguments.parseCMDOptions(["--PENDING_TASKS_SOFT_LIMIT", "35"])
    assert( settings.PENDING_TASKS_SOFT_LIMIT == 35)
    
    # invalid value
    cmdArguments.parseCMDOptions(["--PENDING_TASKS_SOFT_LIMIT", "-35"])
    assert( settings.PENDING_TASKS_SOFT_LIMIT == 1)
    
    # default:
    cmdArguments.parseCMDOptions([])
    assert( settings.PENDING_TASKS_SOFT_LIMIT == 100)


def test_REST_API_PORT_setting():
    cmdArguments.parseCMDOptions(["--REST_API_PORT", "3005"])
    assert( settings.REST_API_PORT == 3005)
    
    # shorthand
    cmdArguments.parseCMDOptions(["-p", "3500"])
    assert( settings.REST_API_PORT == 3500)
    
    # default:
    cmdArguments.parseCMDOptions([])
    assert( settings.REST_API_PORT == 12121)


def test_REST_API_VERSION_setting():
    cmdArguments.parseCMDOptions(["--REST_API_VERSION", "1"])
    assert( settings.REST_API_VERSION == 1)
    
    # default:
    cmdArguments.parseCMDOptions([])
    assert( settings.REST_API_VERSION == REST_version_info[0])


def test_SHORT_JOB_MAX_TIME_setting():
    cmdArguments.parseCMDOptions(["--SHORT_JOB_MAX_TIME", "1"])
    assert( settings.SHORT_JOB_MAX_TIME == 1.0)
    
    # default:
    cmdArguments.parseCMDOptions([])
    assert( settings.SHORT_JOB_MAX_TIME == 0.1)
    
        
def test_DEFAULT_TO_HUMAN_READABLE_NUMBERS_setting():
    cmdArguments.parseCMDOptions(["--DONT_DEFAULT_TO_HUMAN_READABLE_NUMBERS"])
    assert( settings.DEFAULT_TO_HUMAN_READABLE_NUMBERS == False)
    
    # default:
    cmdArguments.parseCMDOptions([])
    assert( settings.DEFAULT_TO_HUMAN_READABLE_NUMBERS == True)