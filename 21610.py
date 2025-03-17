import sys 

input = sys.stdin.readline

N,M = map(int,input().strip().split())
array = [list(map(int,input().strip().split())) for _ in range(N)]


command = []

for i in range(M):
    command.append(list(map(int,input().strip().split())))


cloud=[[N-1,0],[N-1,1],[N-2,0],[N-2,1]]

dx = ['empyt',0,-1,-1,-1,0,1,1,1]
dy = ['empyt',-1,-1,0,1,1,1,0,-1]

dx_f = [-1,1,-1,1]
dy_f = [-1,1,1,-1]

for i in range(len(command)):
    clouded = [[0]*N for _ in range(N)]    
    for a in range(len(cloud)):
        nx = cloud[a][0]+command[i][1]*dx[command[i][0]]
        ny = cloud[a][1]+command[i][1]*dy[command[i][0]]
        nx = nx%N
        ny = ny%N
        clouded[nx][ny] = 1
       
        
       
        
        cloud[a] = [nx,ny]
        array[nx][ny] +=1

    for b in range(len(cloud)):
        cnt= 0
        for j in range(4):
            ndx = cloud[b][0] + dx_f[j]
            ndy = cloud[b][1] + dy_f[j]
            
            if 0<=ndx<N and 0<=ndy<N:
                if array[ndx][ndy]!=0:
                    cnt+=1
        array[cloud[b][0]][cloud[b][1]]+=cnt
        
    cloud=[]
    for r in range(N):
        for c in range(N):
            if array[r][c] >=2 and clouded[r][c]!=1:
                array[r][c]-=2
                cloud.append([r,c])

ans = 0
for r in range(N):
    for c in range(N):
        ans+=array[r][c]
        
print(ans)
        
            
            
    
    
    
    
