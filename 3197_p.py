import sys 
from collections import deque

input = sys.stdin.readline

R, C = map(int,input().strip().split())

target = []
array = []
for l in range(R):
    row = list(input().strip())
    for i in range(C):
        if row[i] == 'L':
            row[i] = 2
            target.append([l, i])
        elif row[i] == '.':
            row[i] = 0
        elif row[i] == 'X':
            row[i] = 1
    array.append(list(map(int, row)))

array[target[1][0]][target[1][1]] = 3

dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]

result = 0
visited = [[0] * C for _ in range(R)]
que = deque()

def move(new_ar, target):
    que.clear()
    for i in range(R):
        for j in range(C):
            visited[i][j] = 0
    
    que.append(target[0])
    visited[target[0][0]][target[0][1]] = 1
    
    while que:
        pos = que.popleft()
        
        for s in range(4):
            nx = pos[0] + dx[s]
            ny = pos[1] + dy[s]
            if 0 <= nx < R and 0 <= ny < C and visited[nx][ny] == 0:
                visited[nx][ny] = 1
                if new_ar[nx][ny] == 0:
                    que.append([nx, ny])
                if new_ar[nx][ny] == 3:
                    return True

    return False

gotit = 0
while True:
    # 원본 배열을 인플레이스 업데이트
    melting = []
    for k in range(R):
        for l in range(C):
            if array[k][l] == 0:
                for i in range(4):
                    nx = k + dx[i]
                    ny = l + dy[i]
                    if 0 <= nx < R and 0 <= ny < C and array[nx][ny] == 1:
                        melting.append((nx, ny))
    
    # 녹을 부분만 업데이트
    for nx, ny in melting:
        array[nx][ny] = 0

    if move(array, target):
        gotit = 1
    
    result += 1
    if gotit == 1:
        print(result)
        break