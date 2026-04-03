dx = [-1,0,1,0]
dy = [0,1,0,-1]

N = int(input())

matrix = [list(input()) for _ in range(N)]
ans=0

def get_best():
    global N, matrix 
    best = 0
    
    for i in range(N):
        bef = ''
        value = 0
        for j in range(N):
            if bef == matrix[i][j]:
                value+=1
            else:
                value = 1
            bef = matrix[i][j]
            best = max(best,value)
        
    for j in range(N):
        bef = ''
        value = 0
        for i in range(N):
            if bef == matrix[i][j]:
                value+=1
            else:
                value = 1
            bef = matrix[i][j]
            best = max(best,value)
    
    return best

for x in range(N):
    for y in range(N):
        for i in range(4):
            nx = x+dx[i]
            ny = y+dy[i]
            if 0<=nx<N and 0<=ny<N :
                if matrix[x][y] != matrix[nx][ny]:
                    matrix[x][y], matrix[nx][ny] = matrix[nx][ny],matrix[x][y]
                    ans = max(ans,get_best())
                    matrix[x][y], matrix[nx][ny] = matrix[nx][ny],matrix[x][y]


print(ans)