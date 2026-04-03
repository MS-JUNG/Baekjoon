N = int(input())

score = list(map(int,input().split()))

dp = [[1,[]] for _ in range(N)]

for i in range(N):
    dp[i][1]+=[score[i]]
    for j in range(i):
        if score[j]<score[i]:
            if dp[j][0]+1 > dp[i][0]:
                dp[i][1] = dp[j][1]+[score[i]]
                dp[i][0] = dp[j][0]+1



dp.sort(reverse=True)
print(dp[0][0])
print(" ".join(map(str,dp[0][1])))
    
