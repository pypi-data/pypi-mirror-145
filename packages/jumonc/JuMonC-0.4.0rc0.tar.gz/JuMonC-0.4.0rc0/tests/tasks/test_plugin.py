import pytest

from JuMonC.tasks import Plugin

def test_error():
    with pytest.raises(Exception):
        p = Plugin.Plugin()
        assert p.isWorking()