import sys 
from itertools import combinations
from collections import deque

input = sys.stdin.readline
N,M = map(int,input().strip().split())

array = [list(map(int,input().strip().split())) for _ in range(N) ]

virus = []
count = 0
k=0
for i  in range(N):
    for j in range(N):
        if array[i][j] == 2:
            virus.append([i,j])
        if array[i][j] == 1:
            count +=1
        if array[i][j] == 0:
            k+=1
target = N*N-count
virus_pos = list(combinations(virus,M))

x = [0,1,-1,0]
y = [1,0,0,-1]
max_list = []

for vir in virus_pos:
    visited = [[0]*N for _ in range(N)]
    
    que = deque()
    for i in range(M):
        que.append(vir[i])
        visited[vir[i][0]][vir[i][1]] = 1
    
    
    
    while que:
        pos = que.popleft()
        # visited[pos[0]][pos[1]] = pos[2]
        
        for i in range(4):
            nx = pos[0]+x[i]
            ny = pos[1]+y[i]
            if  0<=nx<N and 0<=ny<N:
                if array[nx][ny] != 1 and visited[nx][ny]==0:
                    que.append([nx,ny])
                    visited[nx][ny]=visited[pos[0]][pos[1]]+1

    check = 0
    for row in range(N):
        for col in range(N):
            if visited[row][col] == 0:
                check+=1
    
    if check == count:
        for i in range(len(virus)):
            visited[virus[i][0]][virus[i][1]] = 1
        
        max_v = -1
        for row in visited:
            
            if max_v < max(row):
                max_v = max(row)
        max_list.append(max_v)           
        
            

if len(max_list)==0:
    if k==0:
        print(0)
    else:
        print(-1)
else:
    print(min(max_list)-1)
                
                   
                        
            
            
        
        
    

    

            
            



