from JuMonC.tasks import CPU


def test_isWorking():
    plugin = CPU.plugin
    assert(plugin.isWorking)

def test_load():
    plugin = CPU.plugin
    assert(plugin.getLoad(1) > 0)
    assert(plugin.getLoad(5) > 0)
    assert(plugin.getLoad(15) > 0)

def test_getStatusData():
    plugin = CPU.plugin
    assert(len(plugin.getStatusData("load", 1)) == 1)
    assert(len(plugin.getStatusData("none_sense", 1)) == 0)

def test_getConfigData():
    plugin = CPU.plugin
    assert(len(plugin.getConfigData("none_sense", 1)) == 0)