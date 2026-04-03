C = int(input())
G = int(input())

graph = [[] for _ in range(C+1)]

for i in range(G):
    s,e = map(int,input().split())
    graph[s].append(e)
    graph[e].append(s)
    
visited = [0] * (C+1)

def dfs(node,graph):
    
    if visited[node] != 0:
        return 
    
    visited[node] = 1 
    
    for i in graph[node]:
        dfs(i,graph)
        
    return

dfs(1,graph)


print(sum(visited)-1)
    
    
    