from calculadora import soma

def test_soma_positivos():
    assert soma(2, 3) == 5

def test_soma_negativos():
    assert soma(-1, -1) == -2

def test_soma_zero():
    assert soma(0, 0) == 0