from werkzeug.exceptions import NotFound

from JuMonC.handlers import io
from JuMonC.helpers.cmdArguments import parseCMDOptions


def test_ApiPaths():
    version = 1
    link = io.registerRestApiPaths(version)
    assert(( "v" + str(version)) in link["link"])
    assert( "io" in link["link"])
    assert(link["isOptional"] == False)
    
def test_wrongVersionResponse():
    try:
        res = io.returnIOLinks(version = -1)
    except NotFound as e:
        assert( e.code == 404)