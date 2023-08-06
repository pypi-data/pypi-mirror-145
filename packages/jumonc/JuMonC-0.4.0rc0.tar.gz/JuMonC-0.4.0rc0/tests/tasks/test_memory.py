from JuMonC.tasks import memory


def test_isWorking():
    plugin = memory.plugin
    assert(plugin.isWorking)

def test_free():
    plugin = memory.plugin
    assert(plugin.getFree() > 0)

def test_used():
    plugin = memory.plugin
    assert(plugin.getUsed() > 0)

def test_total():
    plugin = memory.plugin
    assert(plugin.getTotal() > 0)

def test_getStatusData():
    plugin = memory.plugin
    assert(len(plugin.getStatusData("free")) == 1)
    assert(len(plugin.getStatusData("used")) == 1)
    assert(len(plugin.getStatusData("used", 1)) == 1)
    assert(len(plugin.getStatusData("used", 1, False)) == 1)
    assert(len(plugin.getStatusData("none_sense", 1)) == 0)

def test_getConfigData():
    plugin = memory.plugin
    assert(len(plugin.getConfigData("total")) == 1)
    assert(len(plugin.getConfigData("none_sense")) == 0)