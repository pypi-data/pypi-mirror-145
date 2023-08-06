from werkzeug.exceptions import NotFound


from JuMonC.helpers.cmdArguments import parseCMDOptions
from JuMonC.handlers import base, main


def test_ApiPaths():
    parseCMDOptions([])
    base.start_version = 1
    base.end_version = 5
    link = main.registerRestApiPaths()
    assert( len(main.links) >= 3 + (base.end_version - base.start_version +1 ) )