from JuMonC.tasks import disk


def test_isWorking():
    plugin = disk.plugin
    assert(plugin.isWorking)

def test_readcount():
    plugin = disk.plugin
    assert(plugin.getReadCount() >= 0)

def test_writecount():
    plugin = disk.plugin
    assert(plugin.getWriteCount() >= 0)

def test_readbytes():
    plugin = disk.plugin
    assert(plugin.getReadBytes() >= 0)

def test_writebytes():
    plugin = disk.plugin
    assert(plugin.getWriteBytes() >= 0)

def test_readtime():
    plugin = disk.plugin
    assert(plugin.getReadTime() >= 0)

def test_writetime():
    plugin = disk.plugin
    assert(plugin.getWriteTime() >= 0)

def test_readMcount():
    plugin = disk.plugin
    assert(plugin.getReadMergedCount() >= 0)

def test_writemcount():
    plugin = disk.plugin
    assert(plugin.getWriteMergedCount() >= 0)

def test_busytime():
    plugin = disk.plugin
    assert(plugin.getBusyTime() >= 0)

def test_getStatusData():
    plugin = disk.plugin
    assert(len(plugin.getStatusData("write_count")) == 1)
    assert(len(plugin.getStatusData("read_count")) == 1)
    assert(len(plugin.getStatusData("write_bytes")) == 1)
    assert(len(plugin.getStatusData("read_bytes")) == 1)
    assert(len(plugin.getStatusData("write_time")) == 1)
    assert(len(plugin.getStatusData("read_time")) == 1)
    assert(len(plugin.getStatusData("write_merged_count")) == 1)
    assert(len(plugin.getStatusData("read_merged_count")) == 1)
    assert(len(plugin.getStatusData("busy_time")) == 1)
    assert(len(plugin.getStatusData("busy_time", 1)) == 1)
    assert(len(plugin.getStatusData("busy_time", 1, False)) == 1)
    assert(len(plugin.getStatusData("none_sense", 1)) == 0)

def test_getConfigData():
    plugin = disk.plugin
    assert(len(plugin.getConfigData("none_sense")) == 0)
