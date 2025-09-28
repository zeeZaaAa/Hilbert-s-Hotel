class Stack:
    def __init__(self, init_list=None):
        if init_list is None:
            self.stack = []
        else:
            self.stack = init_list

    @property
    def pop(self):
        return self.stack.pop()

    def push(self, item):
        self.stack.append(item)

    def peek(self):
        return self.stack[-1] if self.stack else None

    def is_empty(self):
        return len(self.stack) == 0

    def __len__(self):
        return len(self.stack)


class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVL:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def update_height(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def right_rotate(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self.update_height(y)
        self.update_height(x)

        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self.update_height(x)
        self.update_height(y)

        return y

    def rebalance(self, stack: Stack):
        while not stack.is_empty():
            parent = stack.pop
            self.update_height(parent)
            balance = self.get_balance(parent)

            # balance check
            if balance > 1:  # Left
                if self.get_balance(parent.left) < 0:
                    parent.left = self.left_rotate(parent.left)
                new_parent = self.right_rotate(parent)
            elif balance < -1:  # Right
                if self.get_balance(parent.right) > 0:
                    parent.right = self.right_rotate(parent.right)
                new_parent = self.left_rotate(parent)
            else:
                new_parent = parent

            if not stack.is_empty():
                if stack.peek().left == parent:
                    stack.peek().left = new_parent
                else:
                    stack.peek().right = new_parent
            else:
                self.root = new_parent

    def insert(self, key):
        if not self.root:
            self.root = Node(key)
            return

        node = self.root
        stack = Stack()
        while node:
            stack.push(node)
            if key < node.key:
                if not node.left:
                    node.left = Node(key)
                    break
                node = node.left
            elif key >= node.key:
                if not node.right:
                    node.right = Node(key)
                    break
                node = node.right
        self.rebalance(stack)

    def delete(self, key):
        node = self.root
        stack = Stack()
        parent = None

        while node and node.key != key:
            stack.push(node)
            parent = node
            if key < node.key:
                node = node.left
            else:
                node = node.right

        if not node:
            return  # not found

        if node.left and node.right:  # 2 children
            succ_parent = node
            succ = node.right
            while succ.left:
                stack.push(succ)
                succ_parent = succ
                succ = succ.left
            node.key = succ.key
            node = succ
            parent = succ_parent

        # 0 or 1 child
        child = node.left if node.left else node.right
        if parent:
            if parent.left == node:
                parent.left = child
            else:
                parent.right = child
        else:
            self.root = child

        self.rebalance(stack)

    def search(self, key):
        node = self.root
        while node:
            if key == node.key:
                return node
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    def inorder(self):
        result = []
        node = self.root
        stack = Stack([node])
        while not stack.is_empty() or node:
            while node:
                stack.push(node)
                node = node.left
            
            node = stack.pop
            result.append(node.key)
            
            node = node.right
        return result