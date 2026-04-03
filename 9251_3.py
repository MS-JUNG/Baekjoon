N, K = map(int, input().split())
item = [list(map(int, input().split())) for _ in range(N)]

dp = [[0] * (K + 1) for _ in range(N + 1)]

def dfs(c, w):
    if c == N:
        return

    weight, value = item[c]

    # 현재 아이템을 선택하는 경우
    if w + weight <= K:
        if dp[c+1][w + weight] < dp[c][w] + value:
            dp[c+1][w + weight] = dp[c][w] + value
        dfs(c + 1, w + weight)

    # 현재 아이템을 선택하지 않는 경우
    if dp[c+1][w] < dp[c][w]:
        dp[c+1][w] = dp[c][w]
    dfs(c + 1, w)

# 초기 시작
dfs(0, 0)

# 정답 출력
print(max(dp[N]))
