
max_m = 0
def  recur(idx, price):
    global max_m
    if idx ==N-1:
        max_m = max(max_m,price)
        return
    
    if idx >N-1:
        # max_m = max(max_m,price)
        return
    
    recur(idx + interview[idx][0], price + interview[idx][1])
    
    recur(idx + 1, price)


N = int(input())
interview = [list(map(int,input().split())) for _ in range(N)]



recur(0,0)

print(max_m)

## DP 

N = int(input())
interview = [list(map(int, input().split())) for _ in range(N)]

dp = [-1] * (N + 1)

def recur(idx):
    if idx == N:
        return 0
    if idx > N:
        return -10**9
    if dp[idx] != -1:
        return dp[idx]

    t, p = interview[idx]
    dp[idx] = max(recur(idx + 1), p + recur(idx + t))
    return dp[idx]

print(recur(0))