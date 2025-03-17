import sys 
from collections import defaultdict,deque
from itertools import combinations


input = sys.stdin.readline
N = int(input())
pop = list(map(int,input().split()))

edge = defaultdict(list)

for i in range(1,N+1):
    line = list(map(int,input().strip().split()))
    for j in range(line[0]):
        
        edge[i].append(line[j+1])


def bfs(comb):
    sums = 0
    que = deque()
    visited = [0]*(N+1)
    que.append(comb[0])
    visited[comb[0]] =1
    while que:
        target = que.popleft()
        for i in edge[target]:
            if (visited[i] == 0) and (i in comb):
                que.append(i)
                visited[i]=1
            else:
                pass
    
    for k,value in enumerate(visited):
        if value == 1:
            sums += pop[k-1]
    
    visit = sum(visited)
    
    return sums, visit
        
result = 1000
k=0

for i in range(1,N//2+1):
 
    comb_A = list(combinations(range(1,N+1),i))
    for comb in comb_A:
        sum1, v1 = bfs(comb)
        sum2, v2 = bfs([j for j in range(1,N+1) if j not in comb])
        
        if v1 + v2 == N:
            new = abs(sum1-sum2)
            if result > new:
                result = new
            k = 1

if k == 0:
    result = -1
    
    
print(result)
        
    
    
