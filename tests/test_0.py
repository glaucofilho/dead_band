from src import hello_world


def test_hello_world():
    print("TESTE")
    assert hello_world() == "Hello, World!"
