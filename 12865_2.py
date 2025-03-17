N, K = map(int,input().split())

item = [list(map(int,input().split())) for _ in range(N)]


dp = [[-1 for _ in range(K+1)] for _ in range(N)]


def recur(idx,weight):
        if weight > K:
            
            return -999
        if idx == N:
            
            return  0
        
        # if weight > K:
            
        #     return -999
        
        if dp[idx][weight] != -1:
            return dp[idx][weight]  
    
        dp[idx][weight] = max(recur(idx+1, weight+item[idx][0]) +item[idx][1],recur(idx+1,weight))
        
        
        return dp[idx][weight]
    
    
    

answer = recur(0,0)


print(answer )
    
    
    