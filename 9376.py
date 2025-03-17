# import sys 
# import itertools 
# from collections import deque

# input = sys.stdin.readline

# testcase = int(input())

# h, w = map(int,input().strip().split())

# array = [list(input().strip()) for _ in range(h)]

# dx = [0,0,1,-1]
# dy = [1,-1,0,0]

# for k in range(testcase):
    
    
#     h, w = map(int,input().strip().split())

#     array = [list(input().strip()) for _ in range(h)]


#     prison = []
#     door = []

#     for i in range(h):
#         for j in range(w):
#             if array[i][j] == '$':
#                 prison.append([i,j])
#             if array[i][j] == '#':
#                 door.append([i,j])  
        
#     for l in range(0,len(door)+1):
#         k=0
#         if l == 0:         
#             visited = [[0]*w for _ in range(h)]
#             visited_2 = [[0]*w for _ in range(h)]
#             que = deque()
#             que.append(prison[0])
#             while que:
#                 pos = que.popleft()
#                 visited[pos[0]][pos[1]] =1
#                 for ii in range(4):
#                     nx = pos[0] + dx[ii]
#                     ny = pos[1] + dy[ii]
#                     if array[nx][ny] != '*':
#                         if nx == 0 or ny == 0 or nx == h-1 or ny == h-1 or nx == w-1 or ny == w-1:      
#                             result = 0
#                             k += 1   
#                         else: 
#                             que.append([nx,ny])           
#             que = deque()
#             que.append(prison[1])
#             while que:
#                 pos = que.popleft()
#                 visited[pos[0]][pos[1]] =1
#                 for ii in range(4):
#                     nx = pos[0] + dx[ii]
#                     ny = pos[1] + dy[ii]
#                     if array[nx][ny] != '*':
#                         if nx == 0 or ny == 0 or nx == h-1 or ny == h-1 or nx == w-1 or ny == w-1:      
#                             result = 0
#                             k += 1   
#                         else: 
#                             que.append([nx,ny])  
            
#         if k == 2:
#             break
 
#         else:
#             cmb = itertools.combinations(door,l)
#             for case in range(len(cmb)):
#                     cmb[case] 
#                     visited = [[0]*w for _ in range(h)]
#                     visited_2 = [[0]*w for _ in range(h)]
#                     que = deque()
#                     que.append(prison[0])
#                     while que:
#                         pos = que.popleft()
#                         for ii in range(4):
#                             nx = pos[0] + dx[ii]
#                             ny = pos[1] + dy[ii]
            
from collections import deque 
import sys

input = sys.stdin.readline

dx = [1,-1,0,0]
dy = [0,0,1,-1]


def bfs(x,y):
    c = [[-1]* (w+2) for _ in range(h+2)]
    q.append([x,y])
    c[x][y] = 0 
    while q:
        x, y = q.popleft()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            
            if 0<=nx<h+2 and 0<=ny<w+2:
                if c[nx][ny]==-1:
                    if a[nx][ny] == '.':
                        c[nx][ny] = c[x][y]
                        q.appendleft([nx,ny])
                    elif a[nx][ny] == '#': 
                        c[nx][ny] = c[x][y]+1
                        q.append([nx,ny])
        
        return c 

def new_map():
    for i in a:
        i.insert(0, '.')
        i.append('.')
    a.insert(0, ['.' for _ in range(w+2)])
    a.append(['.' for _ in range(w+2)])

tc = int(input())

while tc: 
    h, w = map(int,input().split())
    a = [list(input().strip()) for _ in range(h)]
    q = deque()
    
    new_map()
    
    temp = []
    for i in range(h+2):
        for j in range(w+2):
            if a[i][j] =='$':
                temp.extend([i,j])
                a[i][j] ='.'
    
    x1, y1, x2, y2 = temp 
    c1 = bfs(0,0)
    c2 = bfs(x1, y1)
    c3 = bfs(x2,y2)
    
    ans = sys.maxsize 
    
    for i in range(h+2):
        for j in range(w+2):
            if c1[i][j] != -1 and c2[i][j] != -1 and c3[i][j] != -1:
                cnt = c1[i][j] + c2[i][j] + c3[i][j]
                if a[i][j] == '#':
                    cnt -= 2
                ans = min(ans, cnt)
    print(ans)
    tc -= 1
                
                        
            
        
