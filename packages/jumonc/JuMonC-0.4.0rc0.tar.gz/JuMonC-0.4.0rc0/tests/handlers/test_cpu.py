from werkzeug.exceptions import NotFound

from JuMonC.handlers import cpu
from JuMonC.helpers.cmdArguments import parseCMDOptions


def test_ApiPaths():
    version = 1
    link = cpu.registerRestApiPaths(version)
    assert(( "v" + str(version)) in link["link"])
    assert( "cpu" in link["link"])
    assert(link["isOptional"] == False)
    
def test_wrongVersionResponse():
    try:
        res = cpu.returnCPULinks(version = -1)
    except NotFound as e:
        assert( e.code == 404)