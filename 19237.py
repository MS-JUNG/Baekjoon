import sys 

input = sys.stdin.readline

N, M, K = map(int,input().strip().split())

ocean = [[0]*N for _ in range(N)]

temp = [list(map(int,input().split()) for _ in range(N))]
temp_dir = list(map(int,input().split()))

for i in range(N):
    for j in range(N):
        if temp[i][j] != 0: 
            ocean[i][j] = [temp[i][j]-1, K, temp_dir[temp[i][j]-1]-1]
            
shark_dir = []
for _ in range(M):
    temp = []