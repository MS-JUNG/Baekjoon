import sys
sys.setrecursionlimit(10**6) 
n = int(input())

array = [list(map(int,input().split())) for _ in range(n)]

move = [[0,1],[1,0],[-1,0],[0,-1]]

distance = [[-1 for _ in range(n)] for _ in range(n)]


def find(x,y):

    if distance[x][y] != -1:
        
        return distance[x][y]

    distance[x][y] = 1
    
    for dir in move:
        
        nx,ny = x + dir[0],y+dir[1]
        if  0<= nx < n and 0<=ny<n:
            if array[nx][ny] > array[x][y]:
                distance[x][y] = max(distance[x][y],find(nx,ny) +1)
    
    return distance[x][y]

maxs = 0
for i in range(n):
    for j in range(n):
        
        maxs = max(maxs,find(i,j))
        
        
print(maxs)