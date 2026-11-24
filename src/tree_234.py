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
        if search(self.root, key):
            return False
        
        root = self.root

        if len(root.keys) == 3:
            new_root = Node(leaf=False)
            new_root.children.append(root)
            self.root = new_root
            split_child(new_root, 0)
        self._insert_nonfull(self.root, key)
        return True

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

    def _fix_before_descend(self, node, i):
       
        child = node.children[i]

        if len(child.keys) >= 2:
            return 

        left = node.children[i - 1] if i > 0 else None
        right = node.children[i + 1] if i + 1 < len(node.children) else None

        if left is not None and len(left.keys) >= 2:
            self._borrow_from_left(node, i)

        elif right is not None and len(right.keys) >= 2:
            self._borrow_from_right(node, i)
       
        elif left is not None:
            self._merge(node, i - 1)   
        else:
            self._merge(node, i) 

    def _borrow_from_left(self, parent, i):
       
        child = parent.children[i]
        left = parent.children[i - 1]

        child.keys.insert(0, parent.keys[i - 1])
    
        parent.keys[i - 1] = left.keys.pop()
        
        if not left.leaf:
            child.children.insert(0, left.children.pop())   

    def _borrow_from_right(self, parent, i):
       
        child = parent.children[i]
        right = parent.children[i + 1]
        
        child.keys.append(parent.keys[i])
        
        parent.keys[i] = right.keys.pop(0)

        if not right.leaf:
            child.children.append(right.children.pop(0))   

    def _merge(self, parent, i):
        
        left = parent.children[i]
        right = parent.children[i + 1]

        left.keys.append(parent.keys.pop(i))
        left.keys.extend(right.keys)

        if not left.leaf:
            left.children.extend(right.children)

        parent.children.pop(i + 1)

    def delete(self, key):
        if not search(self.root, key):
            return False          

        self._delete(self.root, key)

        
        if len(self.root.keys) == 0 and not self.root.leaf:
            self.root = self.root.children[0]

        return True

    def _delete(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1


        if i < len(node.keys) and key == node.keys[i]:
            if node.leaf:
                
                node.keys.pop(i)
            else:
                self._delete_from_internal(node, i)
            return
        
        if node.leaf:
            return  

        
        self._fix_before_descend(node, i)
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        self._delete(node.children[i], key)

    def _delete_from_internal(self, node, i):
        left_child = node.children[i]
        right_child = node.children[i + 1]
        target = node.keys[i]                      

        if len(left_child.keys) >= 2:
            pred = self._max_key(left_child)
            node.keys[i] = pred
            self._delete(left_child, pred)
        elif len(right_child.keys) >= 2:
            succ = self._min_key(right_child)
            node.keys[i] = succ
            self._delete(right_child, succ)
        else:
            self._merge(node, i)                   
            self._delete(node.children[i], target)

    def _max_key(self, node):
        while not node.leaf:
            node = node.children[-1]
        return node.keys[-1]

    def _min_key(self, node):
        while not node.leaf:
            node = node.children[0]
        return node.keys[0] 

        
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
    