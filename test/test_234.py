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

if __name__ == "__main__":
    teste_basico()
    teste_stress()