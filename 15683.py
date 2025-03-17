import sys 

input = sys.stdin.readline

N,M = map(int,input().strip().split())

array = [list(map(int,input().strip().split())) for _ in range(M)]
viewed = [[0]*N for _ in range(M)]

for i in range(N):
    for j in range(M):
        if array[i][j]!=0:
            viewed[i][j]=1
        
        
    