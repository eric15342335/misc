class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert_recursively(self.root, value)

    def _insert_recursively(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursively(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursively(node.right, value)

    def inorder_traversal(self):
        self._inorder_traversal_recursively(self.root)
    
    def _inorder_traversal_recursively(self, node):
        if node is not None:
            self._inorder_traversal_recursively(node.left)
            print(node.value, end=" ")
            self._inorder_traversal_recursively(node.right)

    def preorder_traversal(self):
        self._preorder_traversal_recursively(self.root)

    def _preorder_traversal_recursively(self, node):
        if node is not None:
            print(node.value, end=" ")
            self._preorder_traversal_recursively(node.left)
            self._preorder_traversal_recursively(node.right)

    def postorder_traversal(self):
        self._postorder_traversal_recursively(self.root)

    def _postorder_traversal_recursively(self, node):
        if node is not None:
            self._postorder_traversal_recursively(node.left)
            self._postorder_traversal_recursively(node.right)
            print(node.value, end=" ")
    
    def ksmallest(self, k):
        if self is None:
            return k-1, self
        k, node = self.root.left.ksmallest(k)
        if k == 0:
            return self.root
        self.root.right.ksmallest(k)


# Example Usage
if __name__ == "__main__":
    tree = BinaryTree()
    tree.insert(10)
    tree.insert(5)
    tree.insert(15)
    tree.insert(3)

    print(tree.ksmallest(1))