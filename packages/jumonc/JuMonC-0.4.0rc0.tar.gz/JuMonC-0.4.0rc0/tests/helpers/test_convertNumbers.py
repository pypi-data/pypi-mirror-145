from JuMonC.helpers import convertNumbers

def test_convertBinaryPrefix():
    (value, unit) = convertNumbers.convertBinaryPrefix(9999)
    assert(value == "9999")
    assert(unit == "")
    (value, unit) = convertNumbers.convertBinaryPrefix(9999.0)
    assert(value == "9999.00")
    assert(unit == "")
    
    (value, unit) = convertNumbers.convertBinaryPrefix(10240)
    assert(value == "10.00")
    assert(unit == "Ki")
    (value, unit) = convertNumbers.convertBinaryPrefix(10240.0)
    assert(value == "10.00")
    assert(unit == "Ki")
    
    (value, unit) = convertNumbers.convertBinaryPrefix(102400)
    assert(value == "100.00")
    assert(unit == "Ki")
    (value, unit) = convertNumbers.convertBinaryPrefix(102400.0)
    assert(value == "100.00")
    assert(unit == "Ki")