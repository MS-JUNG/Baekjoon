import sys 
from collections import deque

input = sys.stdin.readline
N, M, gas = map(int,input().strip().split())
array = [ list(map(int,input().strip().split())) for _ in range(N)]
taxi = list(map(int,input().strip().split()))
taxi.append(0)
taxi[0]-=1
taxi[1]-=1
customer = {}
cus_map =  [[0]*N for _ in range(N)]

for _ in range(M):
    cust = list(map(int,input().strip().split()))
    customer[(cust[0]-1,cust[1]-1)] = [cust[2]-1,cust[3]-1]
    cus_map[cust[0]-1][cust[1]-1] = 1
    

dx = [0,0,1,-1]
dy = [1,-1,0,0]

k=0
while customer:
    visited = [[0]*N for _ in range(N)]
    que = deque()
    que.append(taxi)
    choose = []
    while que:
        pos = que.popleft()
        
        visited[pos[0]][pos[1]] = 1

        for i in range(4):
            new_x = pos[0] + dx[i]
            new_y = pos[1] + dy[i]
            
            if 0 <= new_x < N and 0 <= new_y < N:  
                if visited[new_x][new_y] == 0 and array[new_x][new_y] !=1:
                    new_cost = pos[2] + 1
                    visited[new_x][new_y] = new_cost
                    que.append([new_x, new_y, new_cost])
                    
                    if cus_map[new_x][new_y] == 1:
                        choose.append([new_x, new_y, new_cost])
                     
                    
    choose.sort(key=lambda x: (x[2],x[0],x[1]))
    if len(choose) == 0 :
        k=1
        print(-1)
        break
    you = choose[0]
    gas-=you[2]
    
    destination = customer[(you[0],you[1])]
    
    del customer[(you[0],you[1])]
    cus_map[you[0]][you[1]]=0
    que = deque()
    que.append([you[0],you[1],0])
    new_visited = [[0]*N for _ in range(N)]
    while que:
        pos = que.popleft()
        new_visited[pos[0]][pos[1]]=1
        if destination == [pos[0],pos[1]]:
            
            break
        else:
            for i in range(4):
                
                new_x = pos[0]+dx[i]
                new_y = pos[1]+dy[i]
                if 0<new_x<N and 0<new_y<N and array[new_x][new_y]!=1:
                    if new_visited[new_x][new_y]==0:
                        new_visited[new_x][new_y] = 1
                        que.append([new_x,new_y,pos[2]+1])
     
    gas-=pos[2]

    if gas < 0:
        k=1
        print(-1)
        break
    gas+=2*pos[2]

    
    taxi = [destination[0],destination[1],0]
        
        
                
             
if k ==0:
    print(gas)     
        
    
    
    
    
