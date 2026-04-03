import sys
input = sys.stdin.readline

N, M, H = map(int, input().split())

# ladder[r][c] = r번 가로 위치에서 c와 c+1 세로선을 연결
ladder = [[False] * (N + 1) for _ in range(H + 1)]

for _ in range(M):
    a, b = map(int, input().split())
    ladder[a][b] = True

answer = 4  # 0~3 안에 못 찾으면 -1 출력


def check():
    # 각 세로선 출발 결과가 자기 자신인지 확인
    for start in range(1, N + 1):
        x = start
        for r in range(1, H + 1):
            if x < N and ladder[r][x]:
                x += 1
            elif x > 1 and ladder[r][x - 1]:
                x -= 1
        if x != start:
            return False
    return True


def dfs(cnt, idx):
    global answer

    # 현재 상태가 이미 정답이면 갱신
    if check():
        answer = min(answer, cnt)
        return

    # 3개 초과 또는 이미 더 나쁜 경우 중단
    if cnt == 3 or cnt >= answer:
        return

    # 1차원 인덱스로 돌면서 중복 탐색 방지
    for k in range(idx, H * (N - 1)):
        r = k // (N - 1) + 1
        c = k % (N - 1) + 1

        # 현재 위치에 가로선을 놓을 수 있는지 확인
        if ladder[r][c]:
            continue
        if c > 1 and ladder[r][c - 1]:
            continue
        if c < N - 1 and ladder[r][c + 1]:
            continue

        ladder[r][c] = True
        dfs(cnt + 1, k + 1)
        ladder[r][c] = False


dfs(0, 0)

print(answer if answer <= 3 else -1)