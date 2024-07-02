import sys 
from collections import deque
import copy
input = sys.stdin.readline
N = int(input().strip())


que = deque()
map = [list(map(int,input().split())) for _ in range(N)]
shark =[]
size = 2
for i in range(N):
    for j in range(N):
        if map[i][j] == 9:
            shark.append(i)
            shark.append(j)
        


def can_move(shark):
    up = [shark[0],shark[1]-1]
    left = [shark[0]-1,shark[1]]
    down = [shark[0],shark[1]+1]
    right = [shark[0]+1,shark[1]]
    
    return up, left,right,down

s = 0
count = 0
s_p = []
while True:
    que = deque()
    que.append(shark)
    new_count = count
    visited = [[0]*N for _ in range(N)]
    visited[shark[0]][shark[1]] = 1
    new_s = copy.copy(s)
    print(new_s)
    while que:
        
        
        u,l,d,r = can_move(que.popleft())
        
   
        if  0 <= u[0]<N and 0 <= u[1]<N and visited[u[0]][u[1]] == 0:
            if 0 <  map[u[0]][u[1]] < size:
                shark = u
                map[u[0]][u[1]] = 9
                count+=1
                s+=1
             
                break
            elif map[u[0]][u[1]] == size or map[u[0]][u[1]] == 0 :
                que.append(u)
                visited[u[0]][u[1]] = 1
            else:
                pass 
        if  0 <= l[0]<N and 0 <= l[1]<N and visited[l[0]][l[1]]==0:
            if 0 <  map[l[0]][l[1]] < size:
                shark = l
                map[l[0]][l[1]] = 9
                count+=1
                s+=1
     
                break
            elif map[l[0]][l[1]] == size or map[l[0]][l[1]] == 0 :
                que.append(l)
                visited[l[0]][l[1]] = 1
            else:
                pass       
        if  0 <= r[0]<N and 0 <= r[1]<N and visited[r[0]][r[1]]==0:
            if 0 < map[r[0]][r[1]] < size:
                shark = r
                map[r[0]][r[1]] = 9
                count+=1
                s+=1
         
                break
            elif map[r[0]][r[1]] == size or map[r[0]][r[1]] == 0 :
                que.append(r)
                visited[r[0]][r[1]] = 1
            else:
                pass        
        if  0 <= d[0]<N and 0 <= d[1]<N and visited[d[0]][d[1]]==0:
            if 0 < map[d[0]][d[1]] < size:
                shark = d
                map[d[0]][d[1]] = 9
                count+=1
                s+=1
                break
            elif map[d[0]][d[1]] == size or map[d[0]][d[1]] == 0 :
                que.append(d)
                visited[d[0]][d[1]] = 1
            else:
                pass

        s+=1
            
    
    if count == size:
        size += 1
        count = 0
    
    if new_count == count:
        
        break                    
        
print(s)