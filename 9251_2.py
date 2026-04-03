import sys 

sys.setrecursionlimit(10**6)


def func(n,m):
    global s1, s2, dp
    
    if n==0 or m==0:    
        return 0
    
    if dp[n][m] != -1:
        return dp[n][m]

    if s1[n] == s2[m]:
        dp[n][m] = func(n-1,m-1)+1
    
    else:
        dp[n][m] = max(func(n-1,m),func(n,m-1))
    
    return dp[n][m]


s1 = input()
s2 = input()

N, M  = len(s1), len(s2)


s1 = " " + s1 
s2 = " " + s2 

dp = [[-1]* (M+1) for _ in range(N+1)]


print(func(N,M))

    
    