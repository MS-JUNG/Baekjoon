N = int(input())

maps = [list(map(int,input().split())) for _ in range(N)]

max_answer = -100
min_answer = 10*9
def dfs(score,idx,layer):
    global max_answer 
    global min_answer 
    
    if layer == N-1:
        score += maps[layer][idx]
        max_answer = max(max_answer,score)
        min_answer = min(min_answer,score)
    
    
    else:
        if idx == 0: 
            dfs(score+maps[layer][idx],idx,layer+1 )
            dfs(score+maps[layer][idx],idx+1,layer+1 )
        elif idx == 1: 
            dfs(score+maps[layer][idx],idx-1,layer+1 )
            dfs(score+maps[layer][idx],idx,layer+1 )
            dfs(score+maps[layer][idx],idx+1,layer+1 )
        else:   
            dfs(score+maps[layer][idx],idx,layer+1 )
            dfs(score+maps[layer][idx],idx-1,layer+1 )
            

dfs(0,0,0)
dfs(0,1,0)
dfs(0,2,0)

print(max_answer, min_answer)
        
        
        
from sys import stdin

N = int(input())
# 맨 처음 세개의 숫자를 입력받아 DP의 초기 값을 설정한다.
arr = list(map(int, stdin.readline().split()))
maxDP = arr
minDP = arr
for _ in range(N - 1):
    arr = list(map(int, stdin.readline().split()))
    # 세가지 값을 입력받을 때마다, DP에 새롭게 갱신한다.
    maxDP = [arr[0] + max(maxDP[0], maxDP[1]), arr[1] + max(maxDP), arr[2] + max(maxDP[1], maxDP[2])]
    minDP = [arr[0] + min(minDP[0], minDP[1]), arr[1] + min(minDP), arr[2] + min(minDP[1], minDP[2])]

print(max(maxDP), min(minDP))    