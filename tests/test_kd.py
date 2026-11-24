import sys
from pathlib import Path

# Adiciona a pasta src ao caminho de importação
ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"
OUT_DIR = ROOT_DIR / "imagens_kd"

sys.path.insert(0, str(SRC_DIR))

from kd_tree import KDTree

OUT_DIR.mkdir(exist_ok=True)

# Problema aplicado: eletropostos num mapa de 20 x 20 km (coordenadas x, y)
eletropostos = [
    (10, 10), (4, 15), (16, 5), (2, 7), (7, 18),
    (13, 14), (18, 11), (6, 3), (1, 12), (9, 6),
    (15, 19), (19, 2), (3, 1), (12, 3), (5, 10),
    (17, 16), (8, 13), (14, 8), (11, 17), (0, 4),
    (20, 9), (6, 8), (15, 12), (3, 19), (18, 6)
]

# ==========================================
# CONSTRUÇÃO BALANCEADA (MEDIANA)
# ==========================================
print("=== CONSTRUÇÃO PELA MEDIANA ===")
tree = KDTree()
tree.build(eletropostos)
print("Quantidade de nós:", tree.size)
print("Altura:", tree.height())
print("Árvore válida?", tree.validate())
tree.plot(OUT_DIR / "01_construcao_mediana.png", "Construção pela mediana (25 eletropostos)")

# Comparação: inserção um a um em ordem crescente (árvore degenerada)
ordenada = KDTree()
for p in sorted(eletropostos):
    ordenada.insert(p)
print("Altura inserindo em ordem crescente:", ordenada.height())

# ==========================================
# INSERÇÃO
# ==========================================
print("\n=== INSERÇÃO ===")
print("Inserindo (12, 11):", tree.insert((12, 11)))
print("Quantidade de nós:", tree.size)
print("Árvore válida?", tree.validate())
tree.plot(OUT_DIR / "02_insercao.png", "Inserção de (12, 11)", highlight=[(12, 11)])

# ==========================================
# ELEMENTO REPETIDO
# ==========================================
# Regra: ponto idêntico é rejeitado; coordenada igual em um só eixo vai à direita (>=)
print("\n=== ELEMENTO REPETIDO ===")
print("Inserção de (10, 10) de novo:", tree.insert((10, 10)))
print("Quantidade de nós:", tree.size)

# ==========================================
# BUSCA
# ==========================================
print("\n=== BUSCA ===")
for p in [(13, 14), (5, 5)]:
    result = tree.search(p)
    print(f"Buscar {p}:", "encontrado" if result else "não encontrado")

# ==========================================
# VIZINHO MAIS PRÓXIMO
# ==========================================
print("\n=== VIZINHO MAIS PRÓXIMO ===")
carro = (7, 8)
node, dist = tree.nearest(carro)
print(f"Carro em {carro}: eletroposto mais próximo {node.point}, a {dist:.2f} km")
tree.plot(OUT_DIR / "03_vizinho_mais_proximo.png",
          f"Vizinho mais próximo do carro em {carro}", highlight=[node.point], query=carro)

# ==========================================
# BUSCA POR REGIÃO
# ==========================================
print("\n=== BUSCA POR REGIÃO ===")
low, high = (5, 5), (12, 14)
dentro = tree.range_search(low, high)
print(f"Eletropostos com x entre {low[0]} e {high[0]} e y entre {low[1]} e {high[1]}:")
print(sorted(dentro))
tree.plot(OUT_DIR / "04_busca_regiao.png", f"Busca por região {low} a {high}",
          highlight=dentro, rect=(low, high))

# ==========================================
# EXCLUSÃO
# ==========================================
print("\n=== EXCLUSÃO ===")
raiz = tree.root.point
print(f"Excluindo a raiz {raiz}:", tree.delete(raiz))
print("Nova raiz:", tree.root.point)
print("Excluindo (3, 1):", tree.delete((3, 1)))
print("Excluindo (5, 5), que não existe:", tree.delete((5, 5)))
print("Quantidade após exclusões:", tree.size)
print("Árvore válida?", tree.validate())
tree.plot(OUT_DIR / "05_exclusao.png", f"Depois de excluir {raiz} e (3, 1)",
          highlight=[tree.root.point])

# ==========================================
# RESULTADOS
# ==========================================
print("\n=== RESULTADOS ===")
print("Altura:", tree.height())
print("Quantidade de nós:", tree.size)
print("Validação final:", tree.validate())
