N, K = map(int, input().split())

item = [list(map(int, input().split())) for _ in range(N)]

dp = [[-1 for _ in range(K + 1)] for _ in range(N)]

def recur(idx, weight):
    if weight > K:
        return -9999  # K를 초과하면 큰 값으로 패널티
    
    if idx == N:
        return 0  # 모든 아이템을 다 확인한 경우
    
    if dp[idx][weight] != -1:
        return dp[idx][weight]  # 이미 계산된 값이 있으면 반환

    # 물건을 담는 경우와 담지 않는 경우 중 최대 가치 선택
    dp[idx][weight] = max(
        recur(idx + 1, weight + item[idx][0]) + item[idx][1],  # 담는 경우
        recur(idx + 1, weight)  # 담지 않는 경우
    )

    return dp[idx][weight]


# 재귀 호출 시작
result = recur(0, 0)

# dp 배열에서 최댓값 찾기
print(result)