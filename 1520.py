import sys
sys.setrecursionlimit(10**6)
N, M = map(int,input().split())

array = [list(map(int,input().split())) for _ in range(N)]

move = [[0,1],[0,-1],[1,0],[-1,0]]



distance = [[-1 for _ in range(M)] for _ in range(N)]

# distance[0][0] = 0
def recur(x,y):
    
    if x == N-1 and y == M-1:
        return 1
    if distance[x][y] != -1:
        return distance[x][y]
    
    route = 0
    for dir in move:
        nx,ny = x+dir[0], y+dir[1]
    
        if  0<=nx<N and 0<=ny<M:
            if array[x][y] > array[nx][ny]:
                
                    route += recur(nx,ny)
          
    distance[x][y] = route
            
    return distance[x][y]

# recur(0,0)
    
print(recur(0,0))