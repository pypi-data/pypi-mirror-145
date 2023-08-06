from werkzeug.exceptions import NotFound

from JuMonC.handlers import job
from JuMonC.helpers.cmdArguments import parseCMDOptions


def test_ApiPaths():
    version = 1
    link = job.registerRestApiPaths(version)
    assert(( "v" + str(version)) in link["link"])
    assert( "job" in link["link"])
    assert(link["isOptional"] == False)
    
def test_wrongVersionResponse():
    try:
        res = job.returnJobLinks(version = -1)
    except NotFound as e:
        assert( e.code == 404)