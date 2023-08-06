from JuMonC.helpers import startup
from JuMonC.models import pluginInformation

def test_findLocalPlugins():
    assert (pluginInformation.slurm_is_working == False)
    assert (pluginInformation.papi_is_working == False)
    assert (pluginInformation.nvidia_is_working == False)
    assert (pluginInformation.network_is_working == False)
    
    startup.findLocalPlugins()

    #assert (pluginInformation.slurm_is_working == True)
    #assert (pluginInformation.papi_is_working == True)
    #assert (pluginInformation.nvidia_is_working == True)
    assert (pluginInformation.network_is_working == True)