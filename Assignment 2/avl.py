from node import Node

def comp_1(root, key):  # For AVL1
    b1=root;b2=key
    if(b1.bin_id==b2.bin_id): return -1
    elif((b1.capacity>b2.capacity) or (b1.capacity==b2.capacity and b1.bin_id>b2.bin_id)):
        return 1  # on left subtree
    elif((b1.capacity<b2.capacity) or (b1.capacity==b2.capacity and b1.bin_id<b2.bin_id)):
        return 0  # On right subtree

def comp_2(root, key): # For AVL2 
    b1=root;b2=key
    if (b1.bin_id==b2.bin_id): return -1
    elif(b1.bin_id> b2.bin_id):
        return 1
    return 0

def comp_3(root, key): # For AVL3
    b1=root;b2=key
    if (b1.object_id==b2.object_id): return -1
    elif(b1.object_id> b2.object_id):
        return 1
    return 0

def comp_4(root, key): # For AVL4
    b1=root;b2=key
    if (b1.bin_id==b2.bin_id): return -1
    elif((b1.capacity>b2.capacity) or (b1.capacity==b2.capacity and b1.bin_id<b2.bin_id)):
        return 1  # on left subtree
    elif((b1.capacity<b2.capacity) or (b1.capacity==b2.capacity and b1.bin_id>b2.bin_id)):
        return 0  # On right subtree

   

class AVLTree:
    def __init__(self, compare_function):
        self.root=None
        self.size=0
        self.comparator=compare_function
        
    def __height(self,node):
        if node is None: return 0
        return node.height
        
    def __rightrotate(self, a):
        b=a.left
        t2=b.right
        
        b.right=a
        a.left=t2
        
        a.height=max(self.__height(a.left), self.__height(a.right))+1
        b.height=max(self.__height(b.left), self.__height(b.right))+1
        return b
        
    def __leftrotate(self, a):
        b=a.right
        t2=b.left
        
        b.left=a
        a.right=t2
        
        a.height=max(self.__height(a.left), self.__height(a.right))+1
        b.height=max(self.__height(b.left), self.__height(b.right))+1
        return b
        
    def __balance(self, node):
        if not node:
            return 0
        return self.__height(node.left)-self.__height(node.right)
        
        
    
    def insert(self, key):
        self.size+=1
        self.root = self.__insert(self.root, key)
        
    def __insert(self, root, key):
        if not root: return Node(key)
        
        if self.comparator(root.data,key):      #on left subtree
            root.left=self.__insert(root.left, key)
        else:                                   #on right subtree
            root.right=self.__insert(root.right, key)

            
        root.height=max(self.__height(root.left), self.__height(root.right))+1
        bal=self.__balance(root)
        
        if bal>1 and self.comparator(root.left.data,key)==1:            #LL
            return self.__rightrotate(root)
            
        if bal<-1 and  self.comparator(root.right.data,key)==0:      #RR
            return self.__leftrotate(root)
        
        if bal>1 and  self.comparator(root.left.data,key)==0:        #LR
            root.left = self.__leftrotate(root.left)
            return self.__rightrotate(root)
            
        if bal<-1 and self.comparator(root.right.data,key)==1:          #RL
            root.right = self.__rightrotate(root.right)
            return self.__leftrotate(root)
        
        return root
        
    def __get_succ(self, node):
        if not node.right:
            return None
        n1 = node.right
        while n1.left:
            n1 = n1.left
        return n1
    
    def deleteNode(self, key):
        self.size-=1
        self.root=self.__deleteNode(self.root, key)
    
    def __deleteNode(self, root, key):
        if not root: return root
    
        if self.comparator(root.data,key)==1:
            root.left = self.__deleteNode(root.left, key)
        elif self.comparator(root.data,key)==0:
            root.right = self.__deleteNode(root.right, key)
        else:
            # if not root.left and not root.right:
            #     return None
            if not root.right:
                return root.left
            elif not root.left:
                return root.right
            else:
                succ=self.__get_succ(root)
                root.data=succ.data
                root.right=self.__deleteNode(root.right, succ.data)
            
        if not root:
            return root
            
        root.height=max(self.__height(root.left),self.__height(root.right))+1
        
        bal=self.__balance(root)
        
        
        if bal>1 and self.__balance(root.left)>=0:    #LL
            return self.__rightrotate(root)
        
        if bal>1 and self.__balance(root.left)<0:     #LR
            root.left=self.__leftrotate(root.left)
            return self.__rightrotate(root)
                

        if bal<-1 and self.__balance(root.right)<=0:  #RR
            return self.__leftrotate(root)

        if bal<-1 and self.__balance(root.right)>0:   #RL
            root.right=self.__rightrotate(root.right)
            return self.__leftrotate(root)
            
        return root
    
    
