import math

class Node:
    def __init__(self, point):
        self.point = point   # tupla (x, y)
        self.left = None     # subárvore esquerda: menor no eixo do nível
        self.right = None    # subárvore direita: maior ou igual


class KDTree:
    def __init__(self, k=2):
        self.k = k           # número de dimensões (2 = x e y)
        self.root = None     # árvore começa vazia
        self.size = 0
    # ==========================================
    # INSERÇÃO
    # ==========================================

    def insert(self, point):
        if self.root is None:              # árvore vazia: vira a raiz
            self.root = Node(point)
            self.size += 1
            return True

        current = self.root
        depth = 0
        while True:
            if point == current.point:     # ponto idêntico: rejeita
                print(f"Ponto {point} já existe na árvore.")
                return False

            axis = depth % self.k          # nível par: x, nível ímpar: y
            if point[axis] < current.point[axis]:
                if current.left is None:   # achou o lugar vazio
                    current.left = Node(point)
                    self.size += 1
                    return True
                next_node = current.left
            else:                          # maior ou igual: direita
                if current.right is None:
                    current.right = Node(point)
                    self.size += 1
                    return True
                next_node = current.right

            current = next_node            # desce um nível
            depth = depth + 1

    # ==========================================
    # BUSCA
    # ==========================================

    def search(self, point):
        current = self.root
        depth = 0
        while current is not None:
            if point == current.point:
                return current
            axis = depth % self.k
            if point[axis] < current.point[axis]:
                current = current.left
            else:
                current = current.right
            depth = depth + 1
        return None                        # caiu num None: não existe

    # ==========================================
    # CONSTRUÇÃO BALANCEADA (MEDIANA)
    # ==========================================

    def build(self, points):
        unique = list(dict.fromkeys(points))   # tira pontos idênticos repetidos
        self.root = self._build(unique, 0)
        self.size = len(unique)

    def _build(self, points, depth):
        if not points:                         # caso base: lista vazia
            return None

        axis = depth % self.k
        points = sorted(points, key=lambda p: p[axis])   # ordena pelo eixo do nível
        mid = len(points) // 2

        # empate no eixo: a esquerda precisa ter só valores MENORES,
        # então recua até o primeiro ponto com o mesmo valor
        while mid > 0 and points[mid - 1][axis] == points[mid][axis]:
            mid -= 1

        node = Node(points[mid])
        node.left = self._build(points[:mid], depth + 1)
        node.right = self._build(points[mid + 1:], depth + 1)
        return node

    # ==========================================
    # ALTURA E VALIDAÇÃO
    # ==========================================

    def height(self):
        def calculate(node):
            if node is None:
                return 0
            return 1 + max(calculate(node.left), calculate(node.right))
        return calculate(self.root)

    def validate(self):
        # cada nó guarda limites herdados dos ancestrais: [mínimo, máximo) por eixo
        def check(node, depth, low, high):
            if node is None:
                return True
            for i in range(self.k):
                if low[i] is not None and node.point[i] < low[i]:
                    return False
                if high[i] is not None and node.point[i] >= high[i]:
                    return False
            axis = depth % self.k
            left_high = list(high);  left_high[axis] = node.point[axis]
            right_low = list(low);   right_low[axis] = node.point[axis]
            return (check(node.left, depth + 1, low, left_high) and
                    check(node.right, depth + 1, right_low, high))
        return check(self.root, 0, [None] * self.k, [None] * self.k)

    # ==========================================
    # VIZINHO MAIS PRÓXIMO
    # ==========================================

    def nearest(self, target):
        best = {"node": None, "dist": float("inf")}   # infinito: qualquer ponto ganha

        def visit(node, depth):
            if node is None:
                return
            # 1. mede o próprio nó
            d = math.dist(target, node.point)
            if d < best["dist"]:
                best["node"], best["dist"] = node, d
            # 2. perto e longe
            axis = depth % self.k
            if target[axis] < node.point[axis]:
                near, far = node.left, node.right
            else:
                near, far = node.right, node.left
            # 3. desce primeiro pelo lado perto
            visit(near, depth + 1)
            # 4. só visita o lado longe se o círculo atravessar o corte
            if abs(target[axis] - node.point[axis]) < best["dist"]:
                visit(far, depth + 1)

        visit(self.root, 0)
        return best["node"], best["dist"]

    # ==========================================
    # BUSCA POR REGIÃO (RETÂNGULO)
    # ==========================================

    def range_search(self, low, high):
        found = []

        def visit(node, depth):
            if node is None:
                return
            # 1. o ponto está dentro do retângulo em todos os eixos?
            if all(low[i] <= node.point[i] <= high[i] for i in range(self.k)):
                found.append(node.point)
            # 2. desce só para os lados que o retângulo alcança
            axis = depth % self.k
            if low[axis] < node.point[axis]:     # esquerda: valores MENORES que o corte
                visit(node.left, depth + 1)
            if high[axis] >= node.point[axis]:   # direita: valores MAIORES OU IGUAIS
                visit(node.right, depth + 1)

        visit(self.root, 0)
        return found

    # ==========================================
    # MENOR VALOR NUM EIXO (USADO NA EXCLUSÃO)
    # ==========================================

    def _minimum(self, node, axis, depth):
        if node is None:
            return None
        if depth % self.k == axis:
            # nó corta pelo mesmo eixo procurado: o menor está à esquerda (ou é ele)
            if node.left is None:
                return node
            return self._minimum(node.left, axis, depth + 1)
        # nó corta por outro eixo: o menor pode estar nos dois lados
        candidates = [node,
                      self._minimum(node.left, axis, depth + 1),
                      self._minimum(node.right, axis, depth + 1)]
        candidates = [c for c in candidates if c is not None]
        return min(candidates, key=lambda c: c.point[axis])

    # ==========================================
    # EXCLUSÃO
    # ==========================================

    def delete(self, point):
        if self.search(point) is None:
            print(f"Ponto {point} não está na árvore.")
            return False
        self.root = self._delete(self.root, point, 0)
        self.size -= 1
        return True

    def _delete(self, node, point, depth):
        axis = depth % self.k

        if node.point == point:
            if node.right is not None:
                # substituto: menor valor no eixo do nó, na subárvore direita
                sub = self._minimum(node.right, axis, depth + 1)
                node.point = sub.point
                node.right = self._delete(node.right, sub.point, depth + 1)
            elif node.left is not None:
                # sem direita: usa o menor da esquerda, e a esquerda vira a direita
                sub = self._minimum(node.left, axis, depth + 1)
                node.point = sub.point
                node.right = self._delete(node.left, sub.point, depth + 1)
                node.left = None
            else:
                return None                    # folha: só sai da árvore
            return node

        if point[axis] < node.point[axis]:
            node.left = self._delete(node.left, point, depth + 1)
        else:
            node.right = self._delete(node.right, point, depth + 1)
        return node

    # ==========================================
    # DESENHO (MATPLOTLIB)
    # ==========================================

    def plot(self, filename, title="Árvore k-D", highlight=None, query=None, rect=None):
        """Salva uma figura com o plano dividido (esquerda) e a árvore (direita).
        highlight: lista de pontos para destacar; query: ponto de consulta;
        rect: (low, high) de uma busca por região."""
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle

        highlight = set(highlight or [])
        cor_x, cor_y = "#c0392b", "#2471a3"     # corte em x = vermelho, em y = azul

        points = []
        def collect(node):
            if node:
                points.append(node.point); collect(node.left); collect(node.right)
        collect(self.root)
        if not points:
            print("Árvore vazia: nada para desenhar.")
            return
        xs = [p[0] for p in points] + ([query[0]] if query else [])
        ys = [p[1] for p in points] + ([query[1]] if query else [])
        x0, x1 = min(xs) - 1, max(xs) + 1
        y0, y1 = min(ys) - 1, max(ys) + 1

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17, 7),
                                       gridspec_kw={"width_ratios": [1, 1.4]})

        # plano dividido pelos cortes
        def cuts(node, depth, bx0, bx1, by0, by1):
            if node is None:
                return
            px, py = node.point
            if depth % 2 == 0:
                ax1.plot([px, px], [by0, by1], color=cor_x, lw=1.4)
                cuts(node.left, depth + 1, bx0, px, by0, by1)
                cuts(node.right, depth + 1, px, bx1, by0, by1)
            else:
                ax1.plot([bx0, bx1], [py, py], color=cor_y, lw=1.4)
                cuts(node.left, depth + 1, bx0, bx1, by0, py)
                cuts(node.right, depth + 1, bx0, bx1, py, by1)
        cuts(self.root, 0, x0, x1, y0, y1)
        if rect:
            (lx, ly), (hx, hy) = rect
            ax1.add_patch(Rectangle((lx, ly), hx - lx, hy - ly, color="#27ae60", alpha=.15))
        for p in points:
            ax1.plot(*p, "o", color="#1e8449" if p in highlight else "#222", ms=7, zorder=5)
            ax1.annotate(f"{p}", p, xytext=(4, 4), textcoords="offset points", fontsize=8)
        if query:
            ax1.plot(*query, "*", color="#8e44ad", ms=16, zorder=6)
        ax1.set_xlim(x0, x1); ax1.set_ylim(y0, y1); ax1.set_aspect("equal")
        ax1.grid(alpha=.25); ax1.set_title("Plano (vermelho = corte em x, azul = em y)")

        # árvore: x pela ordem em-ordem, y pela profundidade
        pos, counter = {}, [0]
        def layout(node, depth):
            if node is None:
                return
            layout(node.left, depth + 1)
            pos[id(node)] = (counter[0], -depth); counter[0] += 1
            layout(node.right, depth + 1)
        layout(self.root, 0)

        def draw(node, depth):
            x, y = pos[id(node)]
            for child in (node.left, node.right):
                if child is not None:
                    cx, cy = pos[id(child)]
                    ax2.plot([x, cx], [y, cy], color="#999", zorder=1)
                    draw(child, depth + 1)
            fill = "#a9dfbf" if node.point in highlight else "white"
            ax2.plot(x, y, "o", ms=30, mfc=fill, mew=2,
                     mec=cor_x if depth % 2 == 0 else cor_y, zorder=3)
            ax2.text(x, y, f"{node.point[0]},{node.point[1]}", ha="center", va="center",
                     fontsize=8, zorder=4)
        draw(self.root, 0)
        h = self.height()
        ax2.set_xlim(-1, len(pos)); ax2.set_ylim(-h + 0.4, 0.6)
        ax2.axis("off"); ax2.set_title(f"Árvore ({self.size} nós, altura {h})")

        fig.suptitle(title)
        fig.tight_layout()
        fig.savefig(filename, dpi=130)
        plt.close(fig)
        print(f"Figura salva em {filename}")
