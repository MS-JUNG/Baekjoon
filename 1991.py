

N = int(input())

graph = [[] for _ in range(130)]

for _ in range(N):
    a,b,c = map(str,input().split())
    a = ord(a)
    b = ord(b)
    c = ord(c)
    graph[a].append(b)
    graph[a].append(c)

def recur(node):
    
    if node == 65:
        return
    print(chr(node), end ="")
    recur(graph[node][0])
    recur(graph[node][1])
    # recur()