n = int(input())

score = []

for k in range(n):
    score+=[int(input())]
    

dp = [[0]*n for _ in range(2)]

if n>=2:
    dp[0][0] = score[0]
    dp[0][1] = score[0] + score[1]
    dp[1][1] =  score[1]

    for i in range(2,n):
        dp[0][i] = dp[1][i-1] + score[i]
        dp[1][i] = max(dp[1][i-2],dp[0][i-2]) + score[i]


    print(max(dp[0][n-1],dp[1][n-1]))

elif n == 1: 
    print(score[0])
elif n == 2:
    print(sum(score))
        
