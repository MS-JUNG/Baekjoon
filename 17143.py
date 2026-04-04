import sys

r, c, m = map(int, sys.stdin.readline().rstrip().split())
# 북 - 남 - 동 - 서                                                                       
dx = [-1, 1, 0, 0]
dy = [0, 0, 1, -1]

# 낚시터 상태
graph = [[[] for _ in range(c)] for _ in range(r)]

for _ in range(m):
    x, y, s, d, z = map(int, input().split())
    graph[x - 1][y - 1].append([z, s, d - 1])


def move_shark():
    global graph
    # 이동한 뒤의 상어 상태를 저장할 배열
    board = [[[] for _ in range(c)] for _ in range(r)]

    for i in range(r):
        for j in range(c):
            if graph[i][j]:
                x, y = i, j
                z, s, d = graph[i][j][0]
                s_count = s
                while s_count > 0:
                    nx = x + dx[d]
                    ny = y + dy[d]
                    # 범위 벗어나면
                    if nx < 0 or nx >= r or ny < 0 or ny >= c:
                        # 방향 바꿔서 다시 이동
                        if d in [0, 2]:
                            d += 1
                        elif d in [1, 3]:
                            d -= 1
                        continue
                    # 범위 안 벗어나면
                    else:
                        # 이동
                        x, y = nx, ny
                        s_count -= 1
                # 이동 끝난 상태 저장
                board[x][y].append([z, s, d])

    # 이동 끝난 상태로 갱신
    for i in range(r):
        for j in range(c):
            graph[i][j] = board[i][j]


eat_count = 0

# j(열)이 증가하는 것 자체가 낚시왕이 열을 한 칸씩 이동하는 것과 같음
for j in range(c):
    for i in range(r):
        if len(graph[i][j]) > 0:
            value = graph[i][j][0]
            eat_count += value[0]
            graph[i][j].remove(value)
            break
    
    # 상어 이동
    move_shark()
    
    # 겹치는 상어 제거
    for p in range(r):
        for q in range(c):
            if len(graph[p][q]) > 1:
                # 상어 무게가 내림차순이 되게 정렬
                graph[p][q].sort(reverse=True)
                # 첫번째 상어(젤 무거운 상어) 제외한 나머지 상어 pop
                while len(graph[p][q]) >= 2:
                    graph[p][q].pop()

print(eat_count)