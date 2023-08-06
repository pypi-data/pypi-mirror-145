from werkzeug.exceptions import NotFound

from JuMonC.handlers import versionTree
from JuMonC.helpers.cmdArguments import parseCMDOptions


def test_ApiPaths():
    version = 1
    link = versionTree.registerRestApiPaths(version)
    assert(( "v" + str(version)) in link["link"])
    assert(link["isOptional"] == False)
    assert( len(versionTree.links["v" + str(version)]) == 6)
    
def test_wrongVersionResponse():
    try:
        res = versionTree.returnVersionLinks(version = -1)
    except NotFound as e:
        assert( e.code == 404)