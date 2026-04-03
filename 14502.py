import sys
from itertools import combinations 
import copy
from collections import deque


N, M = map(int,input().split())

array =[list(map(int,input().split())) for _ in range(N)]

virus = []
space = []
for i in range(N):
    for j in range(M):
        if array[i][j] == 2:
            virus.append([i,j])
        
        if array[i][j] == 0:
            space.append([i,j])
            
            
# comb = list(combinations(space,3))
empty_cnt = len(space)
move = [(0,1),(1,0),(-1,0),(0,-1)]
answer = 0
for pos in combinations(space, 3):
    array_new = [row[:] for row in array]
    array_new[pos[0][0]][pos[0][1]] = 1
    array_new[pos[1][0]][pos[1][1]] = 1
    array_new[pos[2][0]][pos[2][1]] = 1
    que = deque(virus)
    infected = 0
    while que:
        x,y  = que.popleft()
      
        for dx, dy in move:
            nx, ny = x + dx, y + dy
            if 0<=nx<N and 0<=ny<M:
                if array_new[nx][ny] == 0:
                    que.append([nx,ny])
                    array_new[nx][ny] = 2
                    infected += 1
    safe = empty_cnt -3 - infected
    
    
    answer = max(safe,answer)
    
print(answer )
    
                    
                    
        
        
        

            