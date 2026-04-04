from collections import deque

N, M, gas = map(int, input().split())
world = [list(map(int, input().split())) for _ in range(N)]

# 택시 시작 위치 (1-based → 0-based)
taxi_row, taxi_col = map(lambda x: int(x) - 1, input().split())

# 승객 정보 (1-based → 0-based)
# 각 원소 = [start_x, start_y, end_x, end_y]
customers = [list(map(lambda x: int(x) - 1, input().split())) for _ in range(M)]

# 방향 (상하좌우)
move = [(0,1), (1,0), (0,-1), (-1,0)]


def bfs_find_all_customers(taxi, customer_list):
    """
    택시 위치에서 모든 승객 출발지까지의 최단거리를 구한 뒤
    (거리, 출발x, 출발y, 도착x, 도착y, 인덱스) 리스트를 리턴한다.
    """
    (tx, ty) = taxi
    queue = deque()
    queue.append((tx, ty))
    visited = [[-1]*N for _ in range(N)]
    visited[tx][ty] = 0

    # 전체 맵에 대해 BFS
    while queue:
        x, y = queue.popleft()
        for dx, dy in move:
            nx, ny = x+dx, y+dy
            if 0 <= nx < N and 0 <= ny < N:
                if visited[nx][ny] == -1 and world[nx][ny] == 0:
                    visited[nx][ny] = visited[x][y] + 1
                    queue.append((nx, ny))

    # 모든 승객까지의 거리 계산 후 정렬
    dist_list = []
    for idx, (sx, sy, ex, ey) in enumerate(customer_list):
        d = visited[sx][sy]
        if d != -1:  # 갈 수 있는 승객만
            dist_list.append((d, sx, sy, ex, ey, idx))
    dist_list.sort()  # (거리 오름차순, x 오름차순, y 오름차순)으로 자동 정렬
    return dist_list


def go_des(info):
    """
    info = (거리, 출발x, 출발y, 도착x, 도착y, index)
    실제 (출발x, 출발y) → (도착x, 도착y)까지 BFS로 이동 거리를 구한다.
    이동 불가 시 None, None 반환.
    """
    _, sx, sy, ex, ey, _ = info
    queue = deque()
    queue.append((sx, sy))
    visited = [[-1]*N for _ in range(N)]
    visited[sx][sy] = 0

    while queue:
        x, y = queue.popleft()
        if x == ex and y == ey:
            return visited[x][y], (x, y)  # 목적지 도달 시 (최단거리, 위치) 반환
        for dx, dy in move:
            nx, ny = x+dx, y+dy
            if 0 <= nx < N and 0 <= ny < N:
                if visited[nx][ny] == -1 and world[nx][ny] == 0:
                    visited[nx][ny] = visited[x][y] + 1
                    queue.append((nx, ny))
    # 목적지에 도달할 수 없으면
    return None, None


taxi = (taxi_row, taxi_col)

while customers:
    # 1) 현재 택시 위치에서 모든 승객까지 거리 측정
    dist_list = bfs_find_all_customers(taxi, customers)
    if not dist_list:
        # 태울 수 있는 승객이 없음 = 모든 승객에게 도달 불가
        print(-1)
        break

    # 2) 가장 가까운 승객 찾기
    near_dist, sx, sy, ex, ey, cust_idx = dist_list[0]

    # 택시가 손님 위치(sx, sy)까지 이동
    if gas < near_dist:
        # 연료 부족
        print(-1)
        break
    # 택시 이동
    gas -= near_dist
    taxi = (sx, sy)

    # 3) 손님 출발지→도착지 BFS
    dist_dest, end_pos = go_des(dist_list[0])
    if dist_dest is None:
        # 목적지로 갈 수 없는 경우
        print(-1)
        break
    if gas < dist_dest:
        # 이동 도중 연료가 바닥
        print(-1)
        break

    # 목적지 도착 후 연료 계산
    gas -= dist_dest
    gas += (dist_dest * 2)

    # 택시 최종 위치 업데이트 (목적지)
    taxi = end_pos

    # 4) 이동 완료된 승객 제거
    customers.pop(cust_idx)

else:
    # 승객을 모두 성공적으로 태워줬다면 남은 연료 출력
    print(gas)
