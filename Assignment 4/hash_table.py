from prime_generator import get_next_size

class HashTable:
    def __init__(self, collision_type, params):
        '''
        Possible collision_type:
            "Chain"     : Use hashing with chaining
            "Linear"    : Use hashing with linear probing
            "Double"    : Use double hashing
        '''
        self.collision_type=collision_type
        self.params=params
        self.z=params[0]
        self.table_size=params[-1]
        self.table = [[] for _ in range(self.table_size)]
        self.filled=0
    
    def insert(self, x):
        pass
    
    def find(self, key):
        pass
    
    def get_slot(self, key):
        return self.polyacc(key,self.z) % self.table_size


    def get_load(self):
        return self.filled/self.table_size
    
    def __str__(self):
        L=[]
        if self.collision_type== "Chain":
            for i in range(self.table_size):
                if not i==0: L.append(' | ')
                if not self.table[i]: L.append("<EMPTY>")         
                for j in range(len(self.table[i])):
                    if not j==0: L.append(' ; ')
                    L.append(self.table[i][j])
                    
        else:
            for i in  range(self.table_size):
                if not i==0: L.append(" | ")
                if not self.table[i]: L.append("<EMPTY>")
                else: L.append(self.table[i][0])
        return "".join(L)
    
    # Functions added by me
    def get_final_slot(self,key):
        x= self.get_slot(key)
        if self.collision_type=="Linear":
            while self.table[x]:
                x= (x+1)%self.table_size
        elif self.collision_type=="Double":
            aux= self.polyacc(key,self.params[1])
            step=self.params[2]- aux%self.params[2]
            while self.table[x] :
                x= (x+step)%self.table_size
        return x


    def convstrtoint(self,x):
        if ord(x)-ord('a')<0:  # Capital Letter
            return 26+ ord(x)-ord('A')
        else:
            return ord(x)-ord('a')
        
    def polyacc(self,str,z):
        str=str.strip()
        n=len(str)
        ans=self.convstrtoint(str[n-1])
        for i in range(n-2,-1,-1):
            ans= ans*z+self.convstrtoint(str[i])
        return ans
    

    
    # TO BE USED IN PART 2 (DYNAMIC HASH TABLE)
    def rehash(self):
        pass
    
# IMPLEMENT ALL FUNCTIONS FOR CLASSES BELOW
# IF YOU HAVE IMPLEMENTED A FUNCTION IN HashTable ITSELF, 
# YOU WOULD NOT NEED TO WRITE IT TWICE
    
class HashSet(HashTable):
    def __init__(self, collision_type, params):
        # Implemented in HashTable
        super().__init__(collision_type,params)
        pass
    
    def insert(self, key):
        if self.collision_type != 'Chain' and self.get_load()==1:
            raise Exception('Table is full')
        if not self.find(key):
            self.filled+=1
            x=self.get_final_slot(key)
            self.table[x].append(key)
        
    
    def find(self, key):
        x=self.get_slot(key)
        if not self.table[x]: return False
        else:
            if self.collision_type=="Chain":
                for b in self.table[x]:
                    if b==key: return True
                return False 
            elif self.collision_type=="Linear":
                if self.table[x][0]== key: return True
                else:
                    j=(x+1)% self.table_size
                    while self.table[j] and self.table[j][0] != key:
                        if j==x : return False
                        j= (j+1)%self.table_size
                    if self.table[j] and self.table[j][0]== key:
                        return True
                    return False
            else:
                if self.table[x][0]== key: return True
                else:
                    aux= self.polyacc(key,self.params[1])
                    step=self.params[2]- aux%self.params[2]
                    j =(x+ step)%self.table_size
                    while self.table[j] and self.table[j][0] != key:
                        if j==x: return False
                        j=(j+step)%self.table_size
                    if self.table[j] and self.table[j][0]==key: return True
                    return False

    
    def get_slot(self, key):
        # Implemented in HashTable
        return super().get_slot(key)
    
    def get_load(self):
        # Implemented in HashTable
        return super().get_load()
    
    def __str__(self):
        # Implemented in HashTable
        return super().__str__()
    
class HashMap(HashTable):
    def __init__(self, collision_type, params):
        # Implemented in HashTable
        super().__init__(collision_type,params)
        pass
    
    def insert(self, x):
        # x = (key, value)
        if self.collision_type != 'Chain' and self.get_load()==1:
            raise Exception('Table is full')
        key= x[0]; val=x[1]   
        if self.find(key) is None :
            self.filled+=1
            slot=self.get_final_slot(key)
            self.table[slot].append(x)
          
    def find(self, key):
        x=self.get_slot(key)
        if not self.table[x]: return None
        else:
            if self.collision_type=="Chain":
                for b in self.table[x]:
                    if b[0]==key: return b[1]
                return None 
            elif self.collision_type=="Linear":
                if self.table[x][0][0]== key: return self.table[x][0][1]
                else:
                    j=(x+1)% self.table_size
                    while self.table[j] and self.table[j][0][0] != key :
                        if j==x: return None
                        j= (j+1)%self.table_size
                    if self.table[j] and self.table[j][0][0]== key:
                        return self.table[j][0][1]
                    return None
            else:
                if self.table[x][0][0]== key: return self.table[x][0][1]
                else:
                    aux= self.polyacc(key,self.params[1])
                    step=self.params[2]- (aux%self.params[2])
                    j =(x+ step)%self.table_size
                    while self.table[j] and self.table[j][0][0] != key:
                        if j==x: return None
                        j=(j+step)%self.table_size
                    if self.table[j]: return self.table[j][0][1]
                    return None
        
    
    def get_slot(self, key):
        # Implemented in HashTable
        return super().get_slot(key)
    
    def get_load(self):
        # Implemented in HashTable
        return super().get_load()
    
    def __str__(self):

        L=[]
        if self.collision_type== "Chain":
            for i in range(self.table_size):
                if not i==0: L.append(' | ')
                if not self.table[i]: L.append("<EMPTY>")         
                for j in range(len(self.table[i])):
                    if not j==0: L.append(' ; ')
                    y=self.table[i][j]
                    L.append(f'({y[0]}, {y[1]})')
                    
        else:
            for i in  range(self.table_size):
                if not i==0: L.append(" | ")
                if not self.table[i]: L.append("<EMPTY>")
                else: 
                    y=self.table[i][0]
                    L.append(f'({y[0]}, {y[1]})')
        return "".join(L)