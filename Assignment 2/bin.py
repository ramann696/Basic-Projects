from node import Node
from avl import *

class Bin:
    def __init__(self, bin_id, capacity):
        self.bin_id=bin_id
        self.capacity=capacity
        self.child= AVLTree(comp_3)

    def add_object(self, object):
        # Implement logic to add an object to this bin
        self.capacity-=object.size
        self.child.insert(object) 

    def search(self, node, id):
        if(node.data.object_id>id):
            return self.search(node.left,id)
        elif(node.data.object_id<id):
            return self.search(node.right,id)
        else:
            return node

    def remove_object(self, object_id):
        # Implement logic to remove an object by ID
        object= self.search(self.child.root,object_id)
        self.capacity+=object.data.size
        self.child.deleteNode(object.data)

