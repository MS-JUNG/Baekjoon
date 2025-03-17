import sys 
import copy

input = sys.stdin.readline

R,C,T = map(int,input().strip().split())

array = [list(map(int,input().strip().split())) for _ in range(R)]

air_pos = []
for i in range(R):
    for j in range(C):
        if array[i][j] == -1:
            air_pos.append([i,j])

dx = [-1,0,1,0] # 상 우 하 좌
dy = [0,1,0,-1]  


def clean(array,a,b):
    x, y = a, 1 
    index = 1 
    temp = 0 
    while True: 
        nx = x + dx[index]
        ny = y + dy[index]
        
        if nx == R or ny == C or nx == -1 or ny==-1:
            index = (index-1)%4
            continue
        if x==a and y==0:
            break
        
        array[x][y], temp = temp, array[x][y]
        x,y = nx,ny
        
    x, y = b, 1 
    index = 1
    temp = 0 
    while True:
        nx = x + dx[index]
        ny = y + dy[index]
        if nx==R or ny == C or nx==-1 or ny==-1: # 벽에 닿았을 때
            index = (index+1)%4
            continue
        if x==b and y==0: # 공기청정기로 다시 돌아옴
            break
        array[x][y], temp = temp, array[x][y] # swap
        x,y = nx, ny
    return array
      
def move(array):
    new_array = [[0]*C for _ in range(R)]
    new_array[air_pos[0][0]][air_pos[0][1]],new_array[air_pos[1][0]][air_pos[1][1]] = -1,-1
    for i in range(R):
        for j in range(C):
            if array[i][j]>0:
                count = 0
                possible = []
                for ii in range(4):
                    nx = i+dx[ii]
                    ny = j+dy[ii]
                    
                    if 0<=nx<R and 0<=ny<C:
                        if array[nx][ny] != -1:
                            count+=1
                            possible.append([nx,ny])
                
                for po in possible:
                    
                    new_array[po[0]][po[1]] += array[i][j]//5
                    
                new_array[i][j] = array[i][j] - array[i][j]//5 * count
                

    return new_array



   


for t in range(T):
    new = move(array)
    array = clean(new,air_pos[0][0],air_pos[1][0])
    breakpoint()

result = 0
for l in range(R):
    for j in range(C):
        result+=array[l][j]
        
breakpoint()
print(result)
    