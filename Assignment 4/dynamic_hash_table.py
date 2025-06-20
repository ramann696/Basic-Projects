from hash_table import HashSet, HashMap
from prime_generator import get_next_size

class DynamicHashSet(HashSet):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # IMPLEMENT THIS FUNCTION
        old_size=self.table_size
        old_table=self.table
        self.table_size=get_next_size()
        self.table=[[] for _ in range(self.table_size)]
        self.filled=0
        if self.collision_type== "Chain":
            for i in range(old_size):
                for j in range(len(old_table[i])):
                    x=old_table[i][j]
                    self.insert(x)
        else:
            for i in range(old_size):
                x=old_table[i]
                if x: self.insert(x[0])
        
    def insert(self, key):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(key)
        
        if self.get_load() >= 0.5:
            self.rehash()
            
            
class DynamicHashMap(HashMap):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # IMPLEMENT THIS FUNCTION
        old_size=self.table_size
        old_table=self.table
        self.table_size=get_next_size()
        self.table=[[] for _ in range(self.table_size)]
        self.filled=0
        if self.collision_type== "Chain":
            for i in range(old_size):
                for j in range(len(old_table[i])):
                    x=old_table[i][j]
                    self.insert(x)
        else:
            for i in range(old_size):
                x=old_table[i]
                if x: self.insert(x[0])
        
    def insert(self, key):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(key)
        
        if self.get_load() >= 0.5:
            self.rehash()