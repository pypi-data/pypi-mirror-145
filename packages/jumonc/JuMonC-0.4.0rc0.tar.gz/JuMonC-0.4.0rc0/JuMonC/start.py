import logging

import mpi4py
from mpi4py import MPI

from threading import Thread

import sys


from JuMonC import settings
from JuMonC._version import __version__
from JuMonC.helpers.startup import communicateAvaiablePlugins
from JuMonC.helpers.cmdArguments import parseCMDOptions



logger = logging.getLogger(__name__)
logging.info("Running JuMonC with version: %s", __version__)

mpi4py.rc.threads = True
mpi4py.rc.thread_level = "funneled"

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

def startJuMonC() -> None:
    parseCMDOptions(sys.argv[1:])
    communicateAvaiablePlugins()

    #pylint: disable=import-outside-toplevel
    if rank == 0:
        from JuMonC.handlers.base import RESTAPI
        from JuMonC.handlers import main
    
        from JuMonC.tasks import mpiroot
    
        main.registerRestApiPaths()
        flask_thread = Thread(target=RESTAPI.run, kwargs={'debug': True, 'port': settings.REST_API_PORT, 'use_reloader': False})
        flask_thread.start()
    
    
        mpiroot.waitForCommands()
    
    
        flask_thread.join()
    
    else:
        from JuMonC.tasks import mpihandler
    
        mpihandler.waitForCommands()
    #pylint: enable=import-outside-toplevel
        