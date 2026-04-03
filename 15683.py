INF = int(1e9)

# 0: 동, 1: 서, 2: 남, 3: 북
dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]

direction = [
    [],
    [[0], [1], [2], [3]],
    [[0, 1], [2, 3]],
    [[0, 2], [2, 1], [1, 3], [3, 0]],
    [[3, 0, 2], [1, 3, 0], [0, 2, 1], [2, 1, 3]],
    [[0, 1, 2, 3]]
]

def watch(x, y, dirs, office):
    changed = []

    for d in dirs:
        nx, ny = x, y

        while True:
            nx += dx[d]
            ny += dy[d]

            if not (0 <= nx < m and 0 <= ny < n):
                break
            if office[nx][ny] == 6:
                break
            if office[nx][ny] == 0:
                office[nx][ny] = '#'
                changed.append((nx, ny))

    return changed

def undo(changed, office):
    for x, y in changed:
        office[x][y] = 0

def dfs(cnt, office):
    global ans

    if cnt == cctv_cnt:
        blind = 0
        for x in range(m):
            for y in range(n):
                if office[x][y] == 0:
                    blind += 1
        ans = min(ans, blind)
        return

    x, y, cctv = q[cnt]

    for dirs in direction[cctv]:
        changed = watch(x, y, dirs, office)
        dfs(cnt + 1, office)
        undo(changed, office)

n, m = map(int, input().split())

# office[x][y] 형태로 저장
office = [[0] * n for _ in range(m)]
q = []
ans = INF

for y in range(n):
    row = list(map(int, input().split()))
    for x in range(m):
        office[x][y] = row[x]
        if 1 <= office[x][y] <= 5:
            q.append((x, y, office[x][y]))

cctv_cnt = len(q)

dfs(0, office)
print(ans)