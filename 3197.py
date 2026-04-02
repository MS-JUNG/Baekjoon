import sys
from collections import deque

input = sys.stdin.readline

R, C = map(int, input().split())
lake = [list(input().strip()) for _ in range(R)]

dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]

swans = []
water_q = deque()
water_visited = [[False] * C for _ in range(R)]

for i in range(R):
    for j in range(C):
        if lake[i][j] != 'X':
            water_q.append((i, j))
            water_visited[i][j] = True
        if lake[i][j] == 'L':
            swans.append((i, j))

swan_q = deque()
next_swan_q = deque()
swan_visited = [[False] * C for _ in range(R)]

sx, sy = swans[0]
ex, ey = swans[1]

swan_q.append((sx, sy))
swan_visited[sx][sy] = True

def move_swan():
    while swan_q:
        x, y = swan_q.popleft()

        if (x, y) == (ex, ey):
            return True

        for d in range(4):
            nx = x + dx[d]
            ny = y + dy[d]

            if 0 <= nx < R and 0 <= ny < C and not swan_visited[nx][ny]:
                swan_visited[nx][ny] = True

                if lake[nx][ny] == 'X':
                    next_swan_q.append((nx, ny))
                else:
                    swan_q.append((nx, ny))

    return False

def melt():
    global water_q
    next_water_q = deque()

    while water_q:
        x, y = water_q.popleft()

        for d in range(4):
            nx = x + dx[d]
            ny = y + dy[d]

            if 0 <= nx < R and 0 <= ny < C and not water_visited[nx][ny]:
                water_visited[nx][ny] = True

                if lake[nx][ny] == 'X':
                    lake[nx][ny] = '.'
                    next_water_q.append((nx, ny))

    water_q = next_water_q

day = 0
while True:
    if move_swan():
        print(day)
        break

    melt()
    swan_q = next_swan_q
    next_swan_q = deque()
    day += 1