from werkzeug.exceptions import NotFound

from JuMonC.handlers import main_memory
from JuMonC.helpers.cmdArguments import parseCMDOptions


def test_ApiPaths():
    version = 1
    link = main_memory.registerRestApiPaths(version)
    assert(( "v" + str(version)) in link["link"])
    assert( "main_memory" in link["link"])
    assert(link["isOptional"] == False)
    
def test_wrongVersionResponse():
    try:
        res = main_memory.returnMainMemoryLinks(version = -1)
    except NotFound as e:
        assert( e.code == 404)