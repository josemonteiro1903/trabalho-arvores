import sys
import os
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from tree_234 import Tree234, search, validate

def teste_basico():
    t = Tree234()
    for k in [10, 20, 30, 40, 50, 60, 70, 80, 90]:
        t.insert(k)
        print(f"inseriu {k}: raiz = {t.root.keys}")

def teste_stress():
    t = Tree234()
    valores = random.sample(range(1000), 200)
    for v in valores:
        t.insert(v)
        validate(t.root)
    for v in valores:
        assert search(t.root, v), f"sumiu {v}"
        print("tudo ok!")

def test_duplicata():
    t = Tree234()
    assert t.insert(10) is True
    assert t.insert(10) is False      
    assert t.root.keys == [10]        
    validate(t.root)

def test_delete_simples():
    t = Tree234()
    for k in [10, 20, 30, 40]:
        t.insert(k)
    
    assert t.root.keys == [20]
    assert t.root.children[0].keys == [10]
    assert t.root.children[1].keys == [30, 40]

    assert t.delete(30) is True
    validate(t.root)
    assert not search(t.root, 30)
    assert search(t.root, 10) and search(t.root, 20) and search(t.root, 40)


def test_delete_folha():
    
    t = Tree234()
    for k in [10, 20, 30]:
        t.insert(k)
    assert t.root.keys == [10, 20, 30]
    assert t.delete(20) is True
    validate(t.root)
    assert t.root.keys == [10, 30]
    assert not search(t.root, 20)


def test_delete_merge():
    
    t = Tree234()
    for k in [10, 20, 30, 40]:
        t.insert(k)
    
    assert t.delete(40) is True
    validate(t.root)
    assert not search(t.root, 40)
    assert search(t.root, 10) and search(t.root, 20) and search(t.root, 30)


def test_delete_interno():
    
    t = Tree234()
    for k in [10, 20, 30, 40, 50, 60, 70]:
        t.insert(k)
    validate(t.root)
    
    assert t.delete(20) is True
    validate(t.root)
    assert not search(t.root, 20)
    for k in [10, 30, 40, 50, 60, 70]:
        assert search(t.root, k), f"sumiu {k}"


def test_delete_inexistente():
    t = Tree234()
    for k in [10, 20, 30]:
        t.insert(k)
    assert t.delete(99) is False
    validate(t.root)


def test_delete_stress():
    import random
    t = Tree234()
    valores = random.sample(range(1000), 200)
    for v in valores:
        t.insert(v)

    random.shuffle(valores)
    removidos = valores[:100]
    restantes = valores[100:]

    for v in removidos:
        assert t.delete(v) is True, f"falhou remover {v}"
        validate(t.root)

    for v in removidos:
        assert not search(t.root, v), f"{v} deveria ter sumido"
    for v in restantes:
        assert search(t.root, v), f"{v} não deveria ter sumido"

if __name__ == "__main__":
    teste_basico()
    teste_stress()


