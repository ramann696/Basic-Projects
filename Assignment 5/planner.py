from flight import Flight

class Queue:
    def __init__(self, capacity):
        
        self.capacity = capacity  
        self.items = [None] * capacity  
        self.front = -1  
        self.rear = -1   
    
    def is_empty(self):
        return self.front == -1

    def is_full(self):
        return (self.rear + 1) % self.capacity == self.front

    def enqueue(self, value):
        if self.is_full():
            return
        if self.is_empty():
            self.front = 0
        self.rear = (self.rear + 1) % self.capacity
        self.items[self.rear] = value

    def dequeue(self):
        if self.is_empty():
            return None
        value = self.items[self.front]
        if self.front == self.rear:
            self.front = -1
            self.rear = -1
        else:
            self.front = (self.front + 1) % self.capacity
        return value
    
    
class Heap:
    '''
    Class to implement a heap with general comparison function
    '''

    def __init__(self, comparison_function, init_array):
        # Write your code here
        self.comparison_function=comparison_function
        self.heaparr=init_array
        self.heapify()
        
    def insert(self, value):        
        # Write your code here
        n=len(self.heaparr)
        self.heaparr.append(value)
        self.upheap(n)
        pass
    
    def extract(self):
        # Write your code here
        n=len(self.heaparr)
        x=self.heaparr[0]
        self.heaparr[0]=self.heaparr[n-1]
        self.heaparr.pop()
        self.downheap(0)
        return x
        
    
    def top(self):
        return self.heaparr[0]
    
    # You can add more functions if you want to
    def downheap(self,i): 
        while True:
            if(2*i+1<len(self.heaparr)):
                child=self.heaparr[2*i+1]
                ind=2*i+1
                if 2*i+2<len(self.heaparr) and self.comparison_function(self.heaparr[2*i+2],self.heaparr[2*i+1]):
                    child=self.heaparr[2*i+2]
                    ind=2*i+2
                if self.comparison_function(child,self.heaparr[i]):
                    self.heaparr[i],self.heaparr[ind]=self.heaparr[ind],self.heaparr[i]
                    i=ind
                else: break # Heapified
            else: break # No Children Available
                
    def upheap(self,i):
        while(i>0):
            par=(i-1)//2
            if self.comparison_function(self.heaparr[i],self.heaparr[par]):
                self.heaparr[i],self.heaparr[par]=self.heaparr[par],self.heaparr[i]
                i=par
            else: break # Heapified

    def heapify(self):
        n=len(self.heaparr)
        for i in range(n//2-1,-1,-1):
            self.downheap(i)
    
    def is_empty(self):
        return len(self.heaparr)==0

def comparisonmin(val1,val2):
        return val1[0]<val2[0]


class Planner: 
    def __init__(self, flights):
        """The Planner
        Args:
            flights (List[Flight]): A list of information of all the flights (objects of class Flight)
        """
        self.m=len(flights)
        self.citiesgraph=[[] for _ in range(2*self.m+1)]  #GraphofCities
        self.flightgraph=[[] for _ in range(self.m+1)]    #GraphofFlights

        for  fli in flights:
            start=fli.start_city
            self.citiesgraph[start].append(fli)
        
        for fli in flights:
            end=fli.end_city
            for fliout in self.citiesgraph[end]:
                if fliout.departure_time- fli.arrival_time >=20:
                    self.flightgraph[fli.flight_no].append(fliout)

    
    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        arrives the earliest
        """
        if start_city==end_city:
            return []
        else:
            flightinfo=[[float('inf'),-1] for _ in range(self.m+1)]  #[steps,prevflight]  Info works as visited array here
            Q=Queue(self.m+1)
            finalflights=[]
            for x in self.citiesgraph[start_city]:
                if x.departure_time>=t1: # and x.arrival_time<=t2:
                    Q.enqueue([1,x,-1])  #[Flightno.onthispath,thisflight,prevflight]
                    flightinfo[x.flight_no][0]=1;flightinfo[x.flight_no][1]=-1
                    while not Q.is_empty():
                        # for _ in range(Q.size()):
                            qpop=Q.dequeue()
                            if qpop[1].end_city== end_city and qpop[1].arrival_time<=t2:
                                finalflights.append(qpop[1])
                            # flightinfo[qpop[1].flight_no][0]=qpop[0];flightinfo[qpop[1].flight_no][1]=qpop[2]
                            for y in self.flightgraph[qpop[1].flight_no]:
                                if qpop[0]+1<flightinfo[y.flight_no][0]:
                                    Q.enqueue([qpop[0]+1,y,qpop[1]])
                                    flightinfo[y.flight_no][0]=qpop[0]+1
                                    flightinfo[y.flight_no][1]=qpop[1]

            steps=float('inf')
            minarrivaltime=float('inf')
            flight=-1
            for x in finalflights:
                if x.arrival_time<=t2 and (steps>flightinfo[x.flight_no][0] or (steps==flightinfo[x.flight_no][0] and minarrivaltime>x.arrival_time)):
                    steps=flightinfo[x.flight_no][0]
                    minarrivaltime=x.arrival_time
                    flight=x
            
            ans=[]
            if flight!=-1:
                ans.append(flight)
                while True:
                    if flightinfo[flight.flight_no][1]==-1: break
                    ans.append(flightinfo[flight.flight_no][1])
                    flight=flightinfo[flight.flight_no][1]
                return ans[::-1]
            else:
                return ans
 
     
    def cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route is a cheapest route
        """
        if start_city==end_city:
            return []
        else:
            flightinfo=[[float('inf'),-1] for _ in range(self.m +1)]  #[cost,prevflight]  Info works as visited array here
            pq=Heap(comparisonmin,[]) #(cost,thisflight,prevflight)
            finalflights=[]

            for x in self.citiesgraph[start_city]:
                if x.departure_time>=t1: 
                    pq.insert([x.fare,x,-1])  #[costofpath,thisflight,prevflight]
                    flightinfo[x.flight_no][0]=x.fare;flightinfo[x.flight_no][1]=-1
                    while not pq.is_empty():
                        qpop=pq.extract()
                        if qpop[1].end_city== end_city and qpop[1].arrival_time<=t2:
                            finalflights.append(qpop[1])
                        # flightinfo[qpop[1].flight_no][0]=qpop[0];flightinfo[qpop[1].flight_no][1]=qpop[2]
                        for y in self.flightgraph[qpop[1].flight_no]:
                            if y.departure_time>=t1 and y.arrival_time<=t2:
                                if qpop[0]+y.fare<flightinfo[y.flight_no][0]:
                                    pq.insert([qpop[0]+y.fare,y,qpop[1]])
                                    flightinfo[y.flight_no][0]=qpop[0]+y.fare;flightinfo[y.flight_no][1]=qpop[1]

            cost=float('inf')
            flight=-1
            for x in finalflights:
                if  cost>flightinfo[x.flight_no][0]:
                    cost=flightinfo[x.flight_no][0]
                    flight=x
            ans=[]
            if flight!=-1:
                ans.append(flight)
                while True:
                    if flightinfo[flight.flight_no][1]==-1: break
                    ans.append(flightinfo[flight.flight_no][1])
                    flight=flightinfo[flight.flight_no][1]
                return ans[::-1]
            else:
                return ans

    
    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        is the cheapest
        """
        if start_city==end_city:
            return []
        else:
            flightinfo=[[[float('inf'),float('inf')],-1] for _ in range(self.m+1)]  #[[steps,cost],prevflight]  Info works as visited array here
            pq=Heap(comparisonmin,[]) #(cost,thisflight,prevflight)
            finalflights=[]

            for x in self.citiesgraph[start_city]:
                if x.departure_time>=t1: 
                    pq.insert([[1,x.fare],x,-1])  #[[steps,costofpath],thisflight,prevflight]
                    flightinfo[x.flight_no][0][0]=1;flightinfo[x.flight_no][0][1]=x.fare;flightinfo[x.flight_no][1]=-1
                    while not pq.is_empty():
                        qpop=pq.extract()
                        if qpop[1].end_city== end_city and qpop[1].arrival_time<=t2:
                            finalflights.append(qpop[1])
                        # flightinfo[qpop[1].flight_no][0][0]=qpop[0][0];flightinfo[qpop[1].flight_no][0][1]=qpop[0][1]
                        # flightinfo[qpop[1].flight_no][1]=qpop[2]
                        for y in self.flightgraph[qpop[1].flight_no]:
                            if  qpop[0][0]+1<flightinfo[y.flight_no][0][0] or (qpop[0][0]+1==flightinfo[y.flight_no][0][0] and qpop[0][1]+y.fare<flightinfo[y.flight_no][0][1]):
                                pq.insert([[qpop[0][0]+1,qpop[0][1]+y.fare],y,qpop[1]])
                                flightinfo[y.flight_no][0][0]=qpop[0][0]+1
                                flightinfo[y.flight_no][0][1]=qpop[0][1]+y.fare
                                flightinfo[y.flight_no][1]=qpop[1]
 

            cost=float('inf')
            steps=float('inf')
            flight=-1
            for x in finalflights:
                if  steps>flightinfo[x.flight_no][0][0] or (steps==flightinfo[x.flight_no][0][0] and cost>flightinfo[x.flight_no][0][1]):
                    steps=flightinfo[x.flight_no][0][0]
                    cost=flightinfo[x.flight_no][0][1]
                    flight=x
            
            ans=[]
            if flight!=-1:
                ans.append(flight)
                while True:
                    if flightinfo[flight.flight_no][1]==-1: break
                    ans.append(flightinfo[flight.flight_no][1])
                    flight=flightinfo[flight.flight_no][1]
                return ans[::-1]
            else:
                return ans
            

