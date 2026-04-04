from collections import deque
import sys

input = sys.stdin.readline

N, M = map(int, input().split())

board = dict()

for _ in range(N):
    x, y = map(int, input().split())
    board[x] = y

for _ in range(M):
    u, v = map(int, input().split())
    board[u] = v

visited = [False] * 101
dist = [0] * 101

q = deque()
q.append(1)
visited[1] = True

while q:
    now = q.popleft()

    if now == 100:
        print(dist[now])
        break

    for dice in range(1, 7):
        nx = now + dice

        if nx > 100:
            continue

        if nx in board:
            nx = board[nx]

        if not visited[nx]:
            visited[nx] = True
            dist[nx] = dist[now] + 1
            q.append(nx)