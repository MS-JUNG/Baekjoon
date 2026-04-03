import sys
from collections import deque

def shortest_path_with_break(board):
    n, m = len(board), len(board[0])
    # visited[x][y][0] : 아직 벽 안 부숨, visited[x][y][1] : 한 번 부섰음
    visited = [[[0]*2 for _ in range(m)] for _ in range(n)]
    
    q = deque()
    q.append((0, 0, 0))        # x, y, broken(0/1)
    visited[0][0][0] = 1       # 시작 칸 거리 1

    dx = (-1, 1, 0, 0)
    dy = (0, 0, -1, 1)

    while q:
        x, y, br = q.popleft()
        dist = visited[x][y][br]

        if x == n-1 and y == m-1:          # 도착
            return dist

        for dir in range(4):
            nx, ny = x + dx[dir], y + dy[dir]
            if 0 <= nx < n and 0 <= ny < m:
                # 벽이 아니고 아직 그 상태로 미방문
                if board[nx][ny] == '0' and visited[nx][ny][br] == 0:
                    visited[nx][ny][br] = dist + 1
                    q.append((nx, ny, br))
                # 벽이고, 아직 안 부쉈을 때
                elif board[nx][ny] == '1' and br == 0 and visited[nx][ny][1] == 0:
                    visited[nx][ny][1] = dist + 1
                    q.append((nx, ny, 1))
        

    return -1      # 불가능

# ────────────────── I/O ──────────────────
input = sys.stdin.readline
N, M = map(int, input().split())
grid = [input().strip() for _ in range(N)]
print(shortest_path_with_break(grid))
