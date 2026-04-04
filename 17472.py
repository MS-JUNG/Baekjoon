import sys
from collections import deque

input = sys.stdin.readline

N, M = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)]

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

# 1. 섬 번호 붙이기
def label_islands():
    island_id = 2

    for i in range(N):
        for j in range(M):
            if board[i][j] == 1:
                q = deque()
                q.append((i, j))
                board[i][j] = island_id

                while q:
                    x, y = q.popleft()
                    for d in range(4):
                        nx = x + dx[d]
                        ny = y + dy[d]

                        if 0 <= nx < N and 0 <= ny < M and board[nx][ny] == 1:
                            board[nx][ny] = island_id
                            q.append((nx, ny))

                island_id += 1

    return island_id - 2  # 섬 개수


# 2. 다리 후보 찾기
def find_bridges(island_count):
    INF = 10**9
    # 섬 번호는 2부터 시작하므로 크기를 조금 넉넉히 잡음
    dist = [[INF] * (island_count + 2) for _ in range(island_count + 2)]

    for i in range(N):
        for j in range(M):
            if board[i][j] >= 2:
                start = board[i][j]

                for d in range(4):
                    length = 0
                    nx = i + dx[d]
                    ny = j + dy[d]

                    while 0 <= nx < N and 0 <= ny < M:
                        if board[nx][ny] == start:
                            break

                        if board[nx][ny] == 0:
                            length += 1
                            nx += dx[d]
                            ny += dy[d]
                            continue

                        # 다른 섬을 만남
                        end = board[nx][ny]
                        if length >= 2:
                            if length < dist[start][end]:
                                dist[start][end] = length
                                dist[end][start] = length
                        break

    edges = []
    for a in range(2, island_count + 2):
        for b in range(a + 1, island_count + 2):
            if dist[a][b] != INF:
                edges.append((dist[a][b], a, b))

    return edges


# Union-Find
def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]

def union(a, b):
    ra = find(a)
    rb = find(b)

    if ra == rb:
        return False

    parent[rb] = ra
    return True


island_count = label_islands()
edges = find_bridges(island_count)
edges.sort()

parent = [i for i in range(island_count + 2)]

total = 0
used = 0

for cost, a, b in edges:
    if union(a, b):
        total += cost
        used += 1

# 섬이 k개면 MST 간선 수는 k-1개
if used == island_count - 1:
    print(total)
else:
    print(-1)