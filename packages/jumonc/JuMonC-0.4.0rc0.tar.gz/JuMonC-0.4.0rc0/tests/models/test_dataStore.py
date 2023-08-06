import pytest

from JuMonC.models import dataStore


def test_ID():
    assert( (dataStore.getNextDataID() - dataStore.getNextDataID()) == -1)
    
def test_Store():
    test1 = True
    test2 = 3
    test3 = [3,5,7]
    test4 = 2.7
    test5 = "test"
    
    test1ID = dataStore.getNextDataID()
    test2ID = dataStore.getNextDataID()
    test3ID = dataStore.getNextDataID()
    test4ID = dataStore.getNextDataID()
    test5ID = dataStore.getNextDataID()
    
    dataStore.addResult(test1ID, test1)
    dataStore.addResult(test2ID, test2)
    
    assert( test1 == dataStore.getResult(test1ID))
    
    dataStore.addResult(test3ID, test3)
    
    assert( test1 == dataStore.getResult(test1ID))
    
    dataStore.removeResult(test1ID)
    
    with pytest.raises(Exception):
        assert dataStore.getResult(test1ID)
    
    dataStore.addResult(test4ID, test4)
    dataStore.addResult(test5ID, test5)
    
    assert( test2 == dataStore.getResult(test2ID))
    assert( test3 == dataStore.getResult(test3ID))
    assert( test4 == dataStore.getResult(test4ID))
    assert( test5 == dataStore.getResult(test5ID))