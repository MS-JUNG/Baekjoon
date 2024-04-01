import sys 
from collections import deque

def move(x):
    
    new = [[x[0],x[1]-1],[x[0]+1,x[1]],[x[0], x[1]+1],[x[0]-1,x[1]]]

    return new

input = sys.stdin.readline
N, K = map(int,input().strip().split())
glass = [list(map(int,input().strip().split())) for _ in range(N)]
S,X,Y = map(int,input().strip().split())

glass_index = []
for i in range(len(glass)):
    for j in range(len(glass[0])):
        if glass[i][j] != 0:
            glass_index.append([i,j,glass[i][j]])
        else:
            pass
glass_index.sort(key=lambda x: x[2])
glass_index = deque(glass_index)
for i in range(S):
    glass_renew = deque()
    while glass_index:
        value = glass_index.popleft()
        new = move(value)
        for j in range(4):
            if new[j][0] < 0 or new[j][0] >= N or new[j][1] < 0 or new[j][1] >= N:
                
                pass
            else:           
                if glass[new[j][0]][new[j][1]] != 0:
                    pass
                else:
                    glass[new[j][0]][new[j][1]] = value[2]
                glass_renew.append([new[j][0],new[j][1],value[2]])
                
    if glass[X-1][Y-1] != 0:
        break
    glass_index = glass_renew

print(glass[X-1][Y-1])


