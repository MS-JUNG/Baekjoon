import sys
from collections import deque

input = sys.stdin.readline

# 상 우 하 좌
dy = [-1, 0, 1, 0]
dx = [0, 1, 0, -1]


def rotate_subgrid(board, size, sy, sx):
    temp = [[0] * size for _ in range(size)]

    for y in range(size):
        for x in range(size):
            temp[x][size - 1 - y] = board[sy + y][sx + x]

    for y in range(size):
        for x in range(size):
            board[sy + y][sx + x] = temp[y][x]


def firestorm(board, board_size, L):
    sub_size = 2 ** L

    # 1. 부분 격자 회전
    if sub_size > 1:
        for sy in range(0, board_size, sub_size):
            for sx in range(0, board_size, sub_size):
                rotate_subgrid(board, sub_size, sy, sx)

    # 2. 얼음 녹이기
    melt = []

    for y in range(board_size):
        for x in range(board_size):
            if board[y][x] == 0:
                continue

            cnt = 0
            for d in range(4):
                ny = y + dy[d]
                nx = x + dx[d]

                if 0 <= ny < board_size and 0 <= nx < board_size:
                    if board[ny][nx] > 0:
                        cnt += 1

            if cnt < 3:
                melt.append((y, x))

    for y, x in melt:
        board[y][x] -= 1


def get_answer(board, board_size):
    visited = [[False] * board_size for _ in range(board_size)]

    total_ice = 0
    max_group = 0

    for y in range(board_size):
        for x in range(board_size):
            total_ice += board[y][x]

    for y in range(board_size):
        for x in range(board_size):
            if board[y][x] == 0 or visited[y][x]:
                continue

            q = deque()
            q.append((y, x))
            visited[y][x] = True
            group_size = 1

            while q:
                cy, cx = q.popleft()

                for d in range(4):
                    ny = cy + dy[d]
                    nx = cx + dx[d]

                    if 0 <= ny < board_size and 0 <= nx < board_size:
                        if not visited[ny][nx] and board[ny][nx] > 0:
                            visited[ny][nx] = True
                            q.append((ny, nx))
                            group_size += 1

            max_group = max(max_group, group_size)

    return total_ice, max_group


def solve():
    N, Q = map(int, input().split())
    board_size = 2 ** N
    board = [list(map(int, input().split())) for _ in range(board_size)]
    levels = list(map(int, input().split()))

    for L in levels:
        firestorm(board, board_size, L)

    total_ice, max_group = get_answer(board, board_size)
    print(total_ice)
    print(max_group)


solve()