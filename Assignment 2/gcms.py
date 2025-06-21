from node import Node
from bin import Bin
from avl import *
from object import Object, Color
from exceptions import NoBinFoundException

class GCMS:
    def __init__(self):
        # Maintain all the Bins and Objects in GCMS
        self.AVL1= AVLTree(comp_1)  #AVL of bins based on Capacity asc. and ID asc.
        self.AVL2= AVLTree(comp_2)  #AVL of bins based on ID's
        self.AVL3= AVLTree(comp_3)  #AVL of objects based on ID's
        self.AVL4= AVLTree(comp_4)  #AVL of bins based in capacity asc. but ID desc.

    def add_bin(self, bin_id, capacity):
        newbin= Bin(bin_id,capacity)
        self.AVL1.insert(newbin)
        self.AVL2.insert(newbin)
        self.AVL4.insert(newbin)


    def add_object(self, object_id, size, color):
        reqnode=None
        if color==Color.BLUE: # Compact Fit,Least ID, use AVL1
            root= self.AVL1.root
            if not root : raise NoBinFoundException
            while True:
                if root.data.capacity>=size:
                    reqnode=root
                    if root.left:  root=root.left
                    else: break 
                else:
                    if root.right: root=root.right
                    else: break

        elif color==Color.YELLOW: # Compact Fit, Max ID, use AVL4
            root= self.AVL4.root
            if not root : raise NoBinFoundException
            while True:
                if root.data.capacity>=size:
                    reqnode=root
                    if root.left:  root=root.left
                    else: break 
                else:
                    if root.right: root=root.right
                    else: break

        elif color==Color.RED: # Largest Fit, Least ID Use AVL4
            root= self.AVL4.root
           
            if not root : raise NoBinFoundException
            while True: 
                if root.right:
                    root=root.right
                else: break
            if(root.data.capacity>=size): reqnode=root
            else: raise NoBinFoundException

     
    
        elif color==Color.GREEN: # Largest Fit, Max ID Use AVL1
            root= self.AVL1.root
            if not root : raise NoBinFoundException
            while True :
                if root.right:
                    root=root.right
                else: break
            if(root.data.capacity>=size): reqnode=root
            else: raise NoBinFoundException
        
        if not reqnode: raise NoBinFoundException

        reqnodedat=reqnode.data
        id1=reqnodedat.bin_id # ID of bin found using Tree 1 or 4
        cap1=reqnodedat.capacity

        #Update AVL1
        self.AVL1.deleteNode(reqnodedat)
        #Update AVL4
        self.AVL4.deleteNode(reqnodedat)
        
        obj=Object(object_id,size,color,id1)
        reqnodedat.add_object(obj) 
        self.AVL3.insert(obj) #Insert Object in AVLTree 3 with correct parent ID 
        #Insert in 1 and 4
        self.AVL1.insert(reqnodedat)
        self.AVL4.insert(reqnodedat)

      


    def delete_object(self, object_id):
        # Implement logic to remove an object from its bin
        node= self.search_object(self.AVL3.root,object_id)  #Find object from AVL3
        size=node.data.size
        par_id=node.data.parent_id
        self.AVL3.deleteNode(node.data)  #Update AVL3

        reqbin=self.search_bin(self.AVL2.root,par_id) #Required Bin from AVL2
        
        id1=par_id
        cap1=reqbin.data.capacity
        reqbindat=reqbin.data
        
        self.AVL1.deleteNode(reqbindat)
        self.AVL4.deleteNode(reqbindat)
        reqbindat.remove_object(object_id)
        #Insert in 1 and 4
        self.AVL1.insert(reqbindat)
        self.AVL4.insert(reqbindat)
        


    def bin_info(self, bin_id):
        # returns a tuple with current capacity of the bin and the list of objects in the bin (int, list[int])
        node= self.search_bin(self.AVL2.root,bin_id)
        bin=node.data
        L=[]
        self.inorder(bin.child.root,L)
        return bin.capacity,L

    def object_info(self, object_id):
        # returns the bin_id in which the object is stored
        obj =self.search_object(self.AVL3.root,object_id)
        return obj.data.parent_id


    


    def inorder(self,root,L):
        if root is None: return
        self.inorder(root.left,L)
        L.append(root.data.object_id)
        self.inorder(root.right,L)

    def search_bin(self,root,bin_id):
        if not root: return root
        if(root.data.bin_id>bin_id): return self.search_bin(root.left,bin_id)
        elif(root.data.bin_id<bin_id): return  self.search_bin(root.right,bin_id)
        else: return root

    def search_object(self,node,object_id):
        if not node: return node
        if(node.data.object_id>object_id): return self.search_object(node.left,object_id)
        elif(node.data.object_id<object_id): return self.search_object(node.right,object_id)
        else: return node

