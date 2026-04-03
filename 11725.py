N = int(input())

graph = [[] for _ in range(N+1)]
parent = [0 for _ in range(N+1)]

for _ in range(N-1):
    a,b = map(int,input().split())
    
    graph[a].append(b)
    graph[b].append(a)
    


 

def recur(node,prv):
    
    
    
    parent[node] = prv
    
    for nxt in graph[node]:
        if nxt == prv:
            continue
        recur(nxt,node)    
    
    
  
    
    
    

recur(1,0)

for i in parent[2:]:
    print(i)
