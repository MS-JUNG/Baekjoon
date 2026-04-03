N, M = map(int,input().split())

maze = [list(map(int,input().split())) for _ in range(N)]

dp = [[-1]*M for _ in range(N)]

dp[0][0] = maze[0][0]
for i in range(1,M): 
    dp[0][i] =  dp[0][i-1] + maze[0][i]
for j in range(1,N):
    dp[j][0] = dp[j-1][0] + maze[j][0]
    
    

for k in range(1,N):
    for l in range(1,M):
        # if dp[k][l] == -1:
            dp[k][l] = max(dp[k-1][l-1],dp[k][l-1],dp[k-1][l]) + maze[k][l]
        
        

print(dp[N-1][M-1])