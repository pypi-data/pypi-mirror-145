from werkzeug.exceptions import NotFound

from JuMonC.handlers import gpu
from JuMonC.helpers.cmdArguments import parseCMDOptions


def test_ApiPaths():
    version = 1
    link = gpu.registerRestApiPaths(version)
    assert(( "v" + str(version)) in link["link"])
    assert( "gpu" in link["link"])
    assert(link["isOptional"] == False)
    
def test_wrongVersionResponse():
    try:
        res = gpu.returnGPULinks(version = -1)
    except NotFound as e:
        assert( e.code == 404)