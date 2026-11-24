class Node:
    def __init__(self, key=None, value=None, color="RED"):
        self.key = key
        self.value = value
        self.color = color

        self.left = None
        self.right = None
        self.parent = None


class RedBlackTree:

    def __init__(self):
        # Nó sentinela: representa as folhas vazias
        self.NIL = Node(color="BLACK")

        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.NIL.parent = self.NIL

        self.root = self.NIL
        self.size = 0

    # ==========================================
    # BUSCA
    # ==========================================

    def search(self, key):
        current = self.root

        while current != self.NIL:
            if key == current.key:
                return current

            elif key < current.key:
                current = current.left

            else:
                current = current.right

        return None

    # ==========================================
    # ROTAÇÃO À ESQUERDA
    # ==========================================

    def left_rotate(self, x):

        y = x.right

        x.right = y.left

        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent

        if x.parent == self.NIL:
            self.root = y

        elif x == x.parent.left:
            x.parent.left = y

        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    # ==========================================
    # ROTAÇÃO À DIREITA
    # ==========================================

    def right_rotate(self, y):

        x = y.left

        y.left = x.right

        if x.right != self.NIL:
            x.right.parent = y

        x.parent = y.parent

        if y.parent == self.NIL:
            self.root = x

        elif y == y.parent.right:
            y.parent.right = x

        else:
            y.parent.left = x

        x.right = y
        y.parent = x

    # ==========================================
    # INSERÇÃO
    # ==========================================

    def insert(self, key, value=None):

        parent = self.NIL
        current = self.root

        # Localiza a posição de inserção
        while current != self.NIL:

            parent = current

            if key == current.key:
                print(f"Chave {key} já existe na árvore.")
                return False

            elif key < current.key:
                current = current.left

            else:
                current = current.right

        # Cria o novo nó
        new_node = Node(key, value, "RED")

        new_node.left = self.NIL
        new_node.right = self.NIL
        new_node.parent = parent

        if parent == self.NIL:
            self.root = new_node

        elif key < parent.key:
            parent.left = new_node

        else:
            parent.right = new_node

        self.size += 1

        # Corrige possíveis violações
        self.insert_fixup(new_node)

        return True

    # ==========================================
    # BALANCEAMENTO APÓS INSERÇÃO
    # ==========================================

    def insert_fixup(self, z):

        while z.parent.color == "RED":

            if z.parent == z.parent.parent.left:

                uncle = z.parent.parent.right

                # Caso 1: tio vermelho
                if uncle.color == "RED":

                    z.parent.color = "BLACK"
                    uncle.color = "BLACK"

                    z.parent.parent.color = "RED"

                    z = z.parent.parent

                else:

                    # Caso 2: configuração triangular
                    if z == z.parent.right:

                        z = z.parent
                        self.left_rotate(z)

                    # Caso 3: configuração linear
                    z.parent.color = "BLACK"
                    z.parent.parent.color = "RED"

                    self.right_rotate(z.parent.parent)

            else:

                uncle = z.parent.parent.left

                # Caso 1: tio vermelho
                if uncle.color == "RED":

                    z.parent.color = "BLACK"
                    uncle.color = "BLACK"

                    z.parent.parent.color = "RED"

                    z = z.parent.parent

                else:

                    # Caso 2: configuração triangular
                    if z == z.parent.left:

                        z = z.parent
                        self.right_rotate(z)

                    # Caso 3: configuração linear
                    z.parent.color = "BLACK"
                    z.parent.parent.color = "RED"

                    self.left_rotate(z.parent.parent)

        self.root.color = "BLACK"

    # ==========================================
    # LOCALIZAR O MENOR ELEMENTO
    # ==========================================

    def minimum(self, node):

        while node.left != self.NIL:
            node = node.left

        return node

    # ==========================================
    # SUBSTITUIR SUBÁRVORE
    # ==========================================

    def transplant(self, u, v):

        if u.parent == self.NIL:
            self.root = v

        elif u == u.parent.left:
            u.parent.left = v

        else:
            u.parent.right = v

        v.parent = u.parent

    # ==========================================
    # EXCLUSÃO
    # ==========================================

    def delete(self, key):

        z = self.root

        while z != self.NIL and z.key != key:

            if key < z.key:
                z = z.left

            else:
                z = z.right

        if z == self.NIL:
            print(f"Chave {key} não encontrada.")
            return False

        y = z
        original_color = y.color

        if z.left == self.NIL:

            x = z.right
            self.transplant(z, z.right)

        elif z.right == self.NIL:

            x = z.left
            self.transplant(z, z.left)

        else:

            y = self.minimum(z.right)
            original_color = y.color

            x = y.right

            if y.parent == z:

                x.parent = y

            else:

                self.transplant(y, y.right)

                y.right = z.right
                y.right.parent = y

            self.transplant(z, y)

            y.left = z.left
            y.left.parent = y

            y.color = z.color

        self.size -= 1

        # Corrige possíveis violações
        if original_color == "BLACK":
            self.delete_fixup(x)

        return True

    # ==========================================
    # BALANCEAMENTO APÓS EXCLUSÃO
    # ==========================================

    def delete_fixup(self, x):

        while x != self.root and x.color == "BLACK":

            if x == x.parent.left:

                sibling = x.parent.right

                # Caso 1: irmão vermelho
                if sibling.color == "RED":

                    sibling.color = "BLACK"
                    x.parent.color = "RED"

                    self.left_rotate(x.parent)

                    sibling = x.parent.right

                # Caso 2: irmão preto com filhos pretos
                if (sibling.left.color == "BLACK" and
                    sibling.right.color == "BLACK"):

                    sibling.color = "RED"
                    x = x.parent

                else:

                    # Caso 3: filho distante preto
                    if sibling.right.color == "BLACK":

                        sibling.left.color = "BLACK"
                        sibling.color = "RED"

                        self.right_rotate(sibling)

                        sibling = x.parent.right

                    # Caso 4: filho distante vermelho
                    sibling.color = x.parent.color
                    x.parent.color = "BLACK"

                    sibling.right.color = "BLACK"

                    self.left_rotate(x.parent)

                    x = self.root

            else:

                sibling = x.parent.left

                # Caso 1: irmão vermelho
                if sibling.color == "RED":

                    sibling.color = "BLACK"
                    x.parent.color = "RED"

                    self.right_rotate(x.parent)

                    sibling = x.parent.left

                # Caso 2: irmão preto com filhos pretos
                if (sibling.right.color == "BLACK" and
                    sibling.left.color == "BLACK"):

                    sibling.color = "RED"
                    x = x.parent

                else:

                    # Caso 3: filho distante preto
                    if sibling.left.color == "BLACK":

                        sibling.right.color = "BLACK"
                        sibling.color = "RED"

                        self.left_rotate(sibling)

                        sibling = x.parent.left

                    # Caso 4: filho distante vermelho
                    sibling.color = x.parent.color
                    x.parent.color = "BLACK"

                    sibling.left.color = "BLACK"

                    self.right_rotate(x.parent)

                    x = self.root

        x.color = "BLACK"

        # A sentinela sempre deve permanecer preta
        self.NIL.color = "BLACK"

    # ==========================================
    # PERCURSO EM ORDEM
    # ==========================================

    def inorder(self):

        result = []

        def traverse(node):

            if node != self.NIL:

                traverse(node.left)

                result.append({
                    "key": node.key,
                    "value": node.value,
                    "color": node.color
                })

                traverse(node.right)

        traverse(self.root)

        return result

    # ==========================================
    # ALTURA DA ÁRVORE
    # ==========================================

    def height(self):

        def calculate(node):

            if node == self.NIL:
                return 0

            return 1 + max(
                calculate(node.left),
                calculate(node.right)
            )

        return calculate(self.root)

    # ==========================================
    # VALIDAÇÃO DAS PROPRIEDADES
    # ==========================================

    def validate(self):

        if self.root == self.NIL:
            return self.size == 0

        if self.root.color != "BLACK":
            return False

        if self.root.parent != self.NIL:
            return False

        def check(node, lower, upper):

            if node == self.NIL:
                return 1

            # Verifica ordenação da árvore
            if lower is not None and node.key <= lower:
                return -1

            if upper is not None and node.key >= upper:
                return -1

            # Verifica referências dos pais
            if node.left != self.NIL and node.left.parent != node:
                return -1

            if node.right != self.NIL and node.right.parent != node:
                return -1

            # Nó vermelho não pode ter filhos vermelhos
            if node.color == "RED":

                if (node.left.color == "RED" or
                    node.right.color == "RED"):
                    return -1

            left_height = check(node.left, lower, node.key)
            right_height = check(node.right, node.key, upper)

            if left_height == -1 or right_height == -1:
                return -1

            # Todos os caminhos devem ter mesma altura negra
            if left_height != right_height:
                return -1

            return left_height + (1 if node.color == "BLACK" else 0)

        return check(self.root, None, None) != -1
