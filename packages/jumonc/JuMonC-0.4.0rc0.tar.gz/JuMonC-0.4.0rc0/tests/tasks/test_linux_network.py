from JuMonC.tasks import LinuxNetwork


test_data = [{'interface': 'lo', 'received': {'Bytes': 30296808868, 'Packets': 9925597, 'Errs': 0, 'Drop': 0, 'Fifo': 0, 'Frame': 0, 'Compressed': 0, 'Multicast': 0}, 'transmitted': {'Bytes': 30296808868, 'Packets': 9925597, 'Errs': 0, 'Drop': 0, 'Fifo': 0, 'Frame': 0, 'Compressed': 0, 'Multicast': 0}}, {'interface': 'enp225s0f0np0', 'received': {'Bytes': 0, 'Packets': 0, 'Errs': 0, 'Drop': 0, 'Fifo': 0, 'Frame': 0, 'Compressed': 0, 'Multicast': 0}, 'transmitted': {'Bytes': 0, 'Packets': 0, 'Errs': 0, 'Drop': 0, 'Fifo': 0, 'Frame': 0, 'Compressed': 0, 'Multicast': 0}}, {'interface': 'enp225s0f1np1', 'received': {'Bytes': 0, 'Packets': 0, 'Errs': 0, 'Drop': 0, 'Fifo': 0, 'Frame': 0, 'Compressed': 0, 'Multicast': 0}, 'transmitted': {'Bytes': 0, 'Packets': 0, 'Errs': 0, 'Drop': 0, 'Fifo': 0, 'Frame': 0, 'Compressed': 0, 'Multicast': 0}}, {'interface': 'eno1', 'received': {'Bytes': 14480425514, 'Packets': 27025577, 'Errs': 6, 'Drop': 0, 'Fifo': 0, 'Frame': 6, 'Compressed': 0, 'Multicast': 77081}, 'transmitted': {'Bytes': 23424149724, 'Packets': 30228869, 'Errs': 0, 'Drop': 0, 'Fifo': 0, 'Frame': 0, 'Compressed': 0, 'Multicast': 0}}, {'interface': 'eno2', 'received': {'Bytes': 0, 'Packets': 0, 'Errs': 0, 'Drop': 0, 'Fifo': 0, 'Frame': 0, 'Compressed': 0, 'Multicast': 0}, 'transmitted': {'Bytes': 0, 'Packets': 0, 'Errs': 0, 'Drop': 0, 'Fifo': 0, 'Frame': 0, 'Compressed': 0, 'Multicast': 0}}, {'interface': 'enp33s0', 'received': {'Bytes': 4460048701958, 'Packets': 3462215440, 'Errs': 7007943, 'Drop': 1804099, 'Fifo': 0, 'Frame': 7007943, 'Compressed': 0, 'Multicast': 13458754}, 'transmitted': {'Bytes': 2682541949869, 'Packets': 2763418224, 'Errs': 0, 'Drop': 0, 'Fifo': 0, 'Frame': 0, 'Compressed': 0, 'Multicast': 0}}, {'interface': 'ib0', 'received': {'Bytes': 102736163162268, 'Packets': 27688284139, 'Errs': 0, 'Drop': 0, 'Fifo': 0, 'Frame': 0, 'Compressed': 0, 'Multicast': 0}, 'transmitted': {'Bytes': 98963885344636, 'Packets': 26079784462, 'Errs': 0, 'Drop': 0, 'Fifo': 0, 'Frame': 0, 'Compressed': 0, 'Multicast': 0}}, {'interface': 'ib0.8001', 'received': {'Bytes': 19203, 'Packets': 123, 'Errs': 0, 'Drop': 0, 'Fifo': 0, 'Frame': 0, 'Compressed': 0, 'Multicast': 0}, 'transmitted': {'Bytes': 1543, 'Packets': 15, 'Errs': 0, 'Drop': 0, 'Fifo': 0, 'Frame': 0, 'Compressed': 0, 'Multicast': 0}}, {'interface': 'ib0.8004', 'received': {'Bytes': 22673, 'Packets': 144, 'Errs': 0, 'Drop': 0, 'Fifo': 0, 'Frame': 0, 'Compressed': 0, 'Multicast': 0}, 'transmitted': {'Bytes': 2166, 'Packets': 21, 'Errs': 0, 'Drop': 0, 'Fifo': 0, 'Frame': 0, 'Compressed': 0, 'Multicast': 0}}, {'interface': 'ib0.8003', 'received': {'Bytes': 23019, 'Packets': 147, 'Errs': 0, 'Drop': 0, 'Fifo': 0, 'Frame': 0, 'Compressed': 0, 'Multicast': 0}, 'transmitted': {'Bytes': 2151, 'Packets': 21, 'Errs': 0, 'Drop': 0, 'Fifo': 0, 'Frame': 0, 'Compressed': 0, 'Multicast': 0}}, {'interface': 'ib0.8002', 'received': {'Bytes': 20958, 'Packets': 134, 'Errs': 0, 'Drop': 0, 'Fifo': 0, 'Frame': 0, 'Compressed': 0, 'Multicast': 0}, 'transmitted': {'Bytes': 2151, 'Packets': 21, 'Errs': 0, 'Drop': 0, 'Fifo': 0, 'Frame': 0, 'Compressed': 0, 'Multicast': 0}}]

def test_isWorking():
    plugin = LinuxNetwork.plugin
    assert(plugin.isWorking)
    

def test_Network_info():
    plugin = LinuxNetwork.plugin
    interfaces = plugin.GetNetworkInfo()
    assert(len(interfaces) > 0)


def test_InterfaceNames():
    plugin = LinuxNetwork.plugin
    a = plugin.getAvaiableInterfaces()
    b = plugin.getAvaiableInterfaces()
    assert(a)
    assert(a == b)

    
def test_networkDescriptions():
    plugin = LinuxNetwork.plugin
    assert(len(plugin.getAvaiableDataTypes()) == len(plugin.getAvaiableDataTypesDescriptions()))
        
def test_reduceInterfaces():
    LinuxNetwork.plugin.getAvaiableInterfaces()
    LinuxNetwork.plugin._interfaces.append("ib0")
    result = LinuxNetwork._reduceInterfaces(test_data, "ib0")
    assert(len(result) == 1)
    assert(result[0]["interface"] == "ib0")
    
def test_reduceDataTypes():
    LinuxNetwork.plugin.getAvaiableInterfaces()
    LinuxNetwork.plugin._interfaces.append("ib0")
    result = LinuxNetwork._reduceInterfaces(test_data, "ib0")
    result = LinuxNetwork._reduceDataTypes(result, "Packets")
    assert(len(result[0]) == 3)
    assert(result[0]["received"]["Packets"] == 27688284139)
    assert(result[0]["transmitted"]["Packets"] == 26079784462)
           
def test_getDataDiff():
    result = LinuxNetwork._getDataDiff(test_data, test_data)
    assert(result[0]["received"]["Packets"] == 0)


def test_divideData():
    LinuxNetwork.plugin.getAvaiableInterfaces()
    LinuxNetwork.plugin._interfaces.append("ib0")
    result = LinuxNetwork._divideData(test_data, 10.0, "/s")
    result = LinuxNetwork._reduceInterfaces(result, "ib0")
    result = LinuxNetwork._reduceDataTypes(result, "Packets/s")
    assert(result[0]["received"]["Packets/s"] >= 2768828413.8 and result[0]["received"]["Packets/s"] <= 27688284140.0)
    assert(result[0]["transmitted"]["Packets/s"] >= 2607978446.1 and result[0]["transmitted"]["Packets/s"] <= 2607978446.4)
    
def test_makeDataHumanReadable():
    LinuxNetwork.plugin.getAvaiableInterfaces()
    LinuxNetwork.plugin._interfaces.append("ib0")
    result = LinuxNetwork._reduceInterfaces(test_data, "ib0")
    result = LinuxNetwork._reduceDataTypes(result, "Packets")
    result = LinuxNetwork._makeDataHumanReadable(result)
    assert(len(result[0]) == 3)
    assert(result[0]["received"]["GiPackets"] == "25.79")
    assert(result[0]["transmitted"]["GiPackets"] == "24.29")
    
    
def test_getData():
    result = LinuxNetwork.plugin.getData("all", 0.1, "all", False)
    assert(len(result) > 0)
    assert(result[0]["interface"])
    assert(result[0]["received"])
    assert(isinstance(result[0]["received"]["Bytes/s"], float))
    assert(result[0]["transmitted"])
    
    result = LinuxNetwork.plugin.getData("all", -1.0, "all", False)
    assert(len(result) > 0)
    assert(result[0]["interface"])
    assert(result[0]["received"])
    assert(isinstance(result[0]["transmitted"]["Bytes"], int))
    assert(result[0]["transmitted"])