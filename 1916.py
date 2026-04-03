import sys
import heapq

input = sys.stdin.readline
INF = int(1e9)

# 입력
n = int(input())        # 도시 개수
m = int(input())        # 버스 개수

graph = [[] for _ in range(n+1)]
for _ in range(m):
    u, v, cost = map(int, input().split())
    graph[u].append((v, cost))

start, end = map(int, input().split())

# 다익스트라 알고리즘
distance = [INF] * (n+1)
queue = []
heapq.heappush(queue, (0, start))  # (비용, 도시)
distance[start] = 0

while queue:
    dist, now = heapq.heappop(queue)

    # 이미 처리된 도시이면 무시
    if distance[now] < dist:
        continue

    for next_node, next_cost in graph[now]:
        cost = dist + next_cost
        if cost < distance[next_node]:
            distance[next_node] = cost
            heapq.heappush(queue, (cost, next_node))

print(distance[end])
