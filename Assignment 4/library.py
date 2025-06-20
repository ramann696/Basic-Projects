import hash_table as ht


class DigitalLibrary:
    # DO NOT CHANGE FUNCTIONS IN THIS BASE CLASS
    def __init__(self):
        pass
    
    def distinct_words(self, book_title):
        pass
    
    def count_distinct_words(self, book_title):
        pass
    
    def search_keyword(self, keyword):
        pass
    
    def print_books(self):
        pass
    
class MuskLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, book_titles, texts):
        self.texts=[]       
        for i in range(len((texts))):     # Create True Copy to not change the input
            self.texts.append(texts[i].copy())

        for i in range(len(texts)):
            self.mergesort(self.texts[i],[0]*len(texts[i]),0,len(texts[i])-1)
        self.dist_texts=[[] for _ in range(len(texts))]
        for i in range(len(texts)):
            self.dist_texts[i].append(self.texts[i][0])
            for j in range(1,len(texts[i])):
                if self.texts[i][j] != self.texts[i][j-1]:
                    self.dist_texts[i].append(self.texts[i][j])

        self.musklib=[]
        for i in range(len(texts)):
            self.musklib.append([book_titles[i],self.dist_texts[i]])
        self.mergesort(self.musklib,[0]*len(texts),0,len(texts)-1)
        
        
    
    def distinct_words(self, book_title):
        ind=self.binsearch(book_title)
        return self.musklib[ind][1]
    
    def count_distinct_words(self, book_title):
        ind=self.binsearch(book_title)
        return len(self.musklib[ind][1])
        
    
    def search_keyword(self, keyword):  # O(k*logD)
        ans=[]
        for i in range(len(self.musklib)):
            if self.keywordsearch(i,keyword) != -1:
                ans.append(self.musklib[i][0])
        return ans

    
    def print_books(self):
        for i in range(len(self.musklib)):
            print(f"{self.musklib[i][0]}:",end=' ')
            for j in range(len(self.musklib[i][1])):
                if j!= 0: print(' | ',end='')
                print(self.musklib[i][1][j],end='')
            print()

    # Functions defined by me !
    def keywordsearch(self,i,keyword): #Search for a keyword in a specified book
        lo=0
        hi=len(self.musklib[i][1])-1
        ans=-1
        while lo<=hi:
            mid=(lo+hi)//2
            if self.musklib[i][1][mid]==keyword:
                ans=mid;break
            elif self.musklib[i][1][mid]< keyword:
                lo=mid+1
            else:
                hi=mid-1
        return ans

    def binsearch(self,book_title): # Binary Search to find a Book, given its Title
        lo=0
        hi=len(self.musklib)-1
        ans=-1
        while lo<=hi:
            mid=(lo+hi)//2
            if self.musklib[mid][0]==book_title:
                ans=mid;break
            elif self.musklib[mid][0]< book_title:
                lo=mid+1
            else:
                hi=mid-1
        return ans

    def merge(self,L,L2,lo,hi):
        hi1=(hi+lo)//2
        lo2=(lo+hi)//2+1
        cnt=lo
        while lo<=hi1 and lo2<=hi:
            if L[lo]<=L[lo2]:
                L2[cnt]=L[lo]
                lo+=1
            else:
                L2[cnt]=L[lo2]
                lo2+=1
            cnt+=1
        while lo <=hi1:
            L2[cnt]=L[lo]
            cnt+=1;lo+=1
        while lo2 <=hi:
            L2[cnt]= L[lo2]
            cnt+=1;lo2+=1 

    def mergesort(self,L,L2,lo,hi):
        if lo< hi:
            self.mergesort(L,L2,lo,(lo+hi)//2)
            self.mergesort(L,L2,(lo+hi)//2+1,hi)
            self.merge(L,L2,lo,hi)
            for i in range(lo,hi+1):
                L[i]=L2[i]



class JGBLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, name, params):
        '''
        name    : "Jobs", "Gates" or "Bezos"
        params  : Parameters needed for the Hash Table:
            z is the parameter for polynomial accumulation hash
            Use (mod table_size) for compression function
            
            Jobs    -> (z, initial_table_size)
            Gates   -> (z, initial_table_size)
            Bezos   -> (z1, z2, c2, initial_table_size)
                z1 for first hash function
                z2 for second hash function (step size)
                Compression function for second hash: mod c2
        '''
        self.name=name ; self.params=params
        if name=="Jobs":
            self.lib= ht.HashMap("Chain",params)
        elif name== "Gates":
            self.lib= ht.HashMap("Linear",params)
        else:
            self.lib= ht.HashMap("Double",params)
        self.books_list=[]  # All book Titles
        
    
    def add_book(self, book_title, text):
        self.books_list.append(book_title)
        if self.name=="Jobs": # HashSet of words in the book !
            bookset=ht.HashSet("Chain",self.params)
        elif self.name=="Gates":
            bookset=ht.HashSet("Linear",self.params)
        else:
            bookset=ht.HashSet("Double",self.params)

        for i in range(len(text)):
            bookset.insert(text[i])
        self.lib.insert((book_title,bookset))
    
    def distinct_words(self, book_title):
        x=self.lib.find(book_title)
        ans=[]
        for i in x.table:
            for j in i:
                ans.append(j)
        return ans       

    def count_distinct_words(self, book_title):
        x=self.lib.find(book_title) 
        return x.filled
    
    def search_keyword(self, keyword):
        ans=[]
        for i in range(len(self.books_list)):
            x=self.lib.find(self.books_list[i])
            if x.find(keyword):
                ans.append(self.books_list[i])
        return ans
    
    def print_books(self):
        for i in self.lib.table:
            for j in i:
                print(f"{j[0]}: ",end='')
                print(j[1])

        

            
            
