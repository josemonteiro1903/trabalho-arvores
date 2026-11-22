import sys
from pathlib import Path

# Adiciona a pasta src ao caminho de importação
ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"

sys.path.insert(0, str(SRC_DIR))

from red_black_tree import RedBlackTree

# Criando a árvore
tree = RedBlackTree()

# Inserindo 25 elementos
values = [
    50, 30, 70, 20, 40,
    60, 80, 10, 25, 35,
    45, 55, 65, 75, 90,
    5, 15, 22, 28, 33,
    38, 42, 48, 85, 95
]

print("=== INSERÇÃO ===")

for value in values:
    tree.insert(value)

print("Quantidade de nós:", tree.size)
print("Árvore válida?", tree.validate())

# Busca
print("\n=== BUSCA ===")

result = tree.search(40)

if result:
    print("Elemento encontrado:", result.key)
else:
    print("Elemento não encontrado.")

# Testando duplicidade
print("\n=== ELEMENTO REPETIDO ===")

print("Inserção:", tree.insert(50))

# Exclusão
print("\n=== EXCLUSÃO ===")

tree.delete(30)
tree.delete(70)

print("Quantidade após exclusões:", tree.size)
print("Árvore válida?", tree.validate())

# Percurso em ordem
print("\n=== PERCURSO EM ORDEM ===")

for node in tree.inorder():
    print(
        f"Chave: {node['key']} | "
        f"Cor: {node['color']}"
    )

# Altura
print("\n=== RESULTADOS ===")

print("Altura:", tree.height())
print("Quantidade de nós:", tree.size)
print("Validação final:", tree.validate())