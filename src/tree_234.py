class Node:
    def __init__(self, leaf = False):
        self.keys = []
        self.children = []
        self.leaf = leaf

    def __repr__(self):
        return f"Node({self.keys})"
    
def search(node, key):
    i = 0
    while i < len(node.keys) and key > node.keys[i]:
        i += 1
    if i < len(node.keys) and key == node.keys[i]:
        return True
    if node.leaf:
        return False
    return search(node.children[i], key)

def split_child(parent, i):
    
    full = parent.children[i]
    mid_key = full.keys[1]

    right = Node(leaf=full.leaf)
    right.keys = full.keys[2:]

    if not full.leaf:
        right.children = full.children[2:]
        full.children = full.children[:2]

    parent.keys.insert(i, mid_key)
    parent.children.insert(i + 1, right)

    full.keys = full.keys[:1]

class Tree234:
    def __init__(self):
        self.root = Node(leaf=True)

    def insert(self, key):
        root = self.root

        if len(root.keys) == 3:
            new_root = Node(leaf=False)
            new_root.children.append(root)
            self.root = new_root
            split_child(new_root, 0)
        self._insert_nonfull(self.root, key)

    def _insert_nonfull(self, node, key):
        if node.leaf:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            node.keys.insert(i, key)
        else:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1

            if len(node.children[i].keys) == 3:
                split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_nonfull(node.children[i], key)
        
def validate(node):
    assert node.keys == sorted(node.keys), f"desordenado: {node.keys}"
    assert len(node.keys) <= 3, f"overflow: {node.keys}"
    if node.leaf:
        return 0
    assert len(node.children) == len(node.keys) + 1, \
        f"filhos errados: {len(node.children)} filhos, {len(node.keys)} chaves"
    heights = [validate(c) for c in node.children]
    assert len(set(heights)) == 1, f"folhas em níveis diferentes: {heights}"
    return heights[0] + 1
    