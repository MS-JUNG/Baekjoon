import sys 

sys.setrecursionlimit(1000000)
input = sys.stdin.readline

N, M, R = map(int, input().strip().split())


edge = [list(map(int,(input().strip().split()))) for _ in range(M)]
edge_dict = {}

for i in range(1,N+1):
    edge_dict[i] = []

for i in range(len(edge)):
    edge_dict[edge[i][0]].append(edge[i][1])
    
    edge_dict[edge[i][1]].append(edge[i][0])    

for i in edge_dict.keys():
    edge_dict[i].sort()
visited = [0]*N
sequence = [0]*N


value = 1
def dfs(visited, edge_dict,R):
    global value 
    if visited[R-1] == 1:
         return True
    else:
        visited[R-1] = 1
    if sequence[R-1] != 0:
        pass
    else:
        sequence[R-1] = value
    
 
    for i in range(len(edge_dict[R])):
        R_1 = edge_dict[R][i]
        if visited[R_1-1] == 1:
            pass
        else:
            
            value += 1
            
            dfs(visited,edge_dict,R_1)
    return True


dfs(visited,edge_dict,R)

for i in range(len(sequence)):
     print(sequence[i])

