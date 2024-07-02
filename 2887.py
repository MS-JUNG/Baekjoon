import sys 

input = sys.stdin.readline
def find_parent(parents, x):
    if parents[x] != x:
        parents[x] = find_parent(parents, parents[x])
        
    return parents[x]


def union_parents(parents, a,b):
    a = find_parent(parents,a)
    b = find_parent(parents,b)
    
    if a<b:
        parents[b] = a 
        
    else:
        parents[a] = b

n = input()
parents = [i for i in range(n)]
x = []
y = []
z = []
edges = []

for i in range(n):
    data = list(map(int,input().split()))
    x.append((data[0],i))
    y.append((data[1],i))
    z.append((data[2],i))

x.sort()
y.sort()
z.sort()

for i in range(n-1):
    edges.append((x[i+1][0]-x[i][0],x[i][1],x[i+1][1]))
    edges.append((y[i+1][0]-x[i][0],y[i][1],y[i+1][1]))
    edges.append((z[i+1][0]-z[i][0],x[i][1],z[i+1][1]))
    
    

edges.sort()
result = 0 

for e in edges: 
    if find_parent(parents,e[1]) != find_parent(parents,e[2]):
        result += e[0]
        union_parents(parents,e[1],e[2])

print(result)