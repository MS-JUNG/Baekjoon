import sys 
from collections import deque

input = sys.stdin.readline

N,L,R = map(int,input().strip().split())

array = [list(map(int,input().strip().split())) for _ in range(N)]

dx = [0,1,-1,0]
dy = [1,0,0,-1]
result = 0
while True:
    visited = [[0]*N for _ in range(N)]
    
    while  sum(sum(row) for row in visited) != N * N:
    
        finish = 0
        for i in range(N):
            for j  in range(N):
                
                if visited[i][j] == 0: 
                    finish+=1
                    que = deque()
                    que.append([i,j])
                    visited[i][j]=1
                    cluster = []
                    count = 0
                    summation = 0 
                    while que:
                        
                        
                        pos = que.popleft()
                        summation += array[pos[0]][pos[1]]
                        count+=1
                        
                        cluster.append(pos)
                        for m in range(4):
                            nx = pos[0]+dx[m]
                            ny = pos[1]+dy[m]
                            if 0<=nx<N and 0<=ny<N and visited[nx][ny]==0 and L<=abs(array[pos[0]][pos[1]]-array[nx][ny])<=R:
                                que.append([nx,ny])
                              
                                visited[nx][ny] = 1
          
                    population = summation//count
                    for k in range(len(cluster)):
                        array[cluster[k][0]][cluster[k][1]] = population


    if finish == N*N:
            
                break        
    else:
        result+=1     

print(result)
    
                                
                        
        
    