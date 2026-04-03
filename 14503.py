import sys
input = sys.stdin.readline

N, M = map(int, input().split())
r, c, d = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)]

# 북, 동, 남, 서
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

count = 0

while True:
    # 1. 현재 칸 청소
    if board[r][c] == 0:
        board[r][c] = 2
        count += 1

    # 2. 주변 4칸 중 청소되지 않은 빈칸 있는지 확인
    found = False
    for i in range(4):
        nr = r + dr[i]
        nc = c + dc[i]
        if board[nr][nc] == 0:
            found = True
            break

    if not found:
        # 2-1. 후진
        back_dir = (d + 2) % 4
        br = r + dr[back_dir]
        bc = c + dc[back_dir]

        if board[br][bc] != 1:
            r, c = br, bc
        else:
            # 2-2. 뒤가 벽이면 종료
            break
    else:
        # 3-1. 반시계 90도 회전
        d = (d + 3) % 4

        # 3-2. 앞칸이 청소되지 않은 빈칸이면 전진
        nr = r + dr[d]
        nc = c + dc[d]
        if board[nr][nc] == 0:
            r, c = nr, nc

print(count)