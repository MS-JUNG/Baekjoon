from itertools import combinations

# 백트래킹
def dfs(depth):
    global cnt
    
    # 15번째 경기에 도달했을 때
    if depth == 15:
        cnt = 1
        for sub in res:
            # 전체 승무패의 합계가 0이 아니면
            if sub.count(0) != 3:
                cnt = 0
                break
        return
    
    # 전체 경기 15번의 조합
    g1, g2 = games[depth]
    # 각 경기의 승무패
    for x, y in ((0,2), (1,1), (2,0)):
        if res[g1][x] > 0 and res[g2][y] > 0:
            res[g1][x] -= 1
            res[g2][y] -= 1
            dfs(depth+1)
            res[g1][x] += 1
            res[g2][y] += 1

if __name__ == "__main__":
    answers = []
    games = list(combinations(range(6), 2))

    for _ in range(4):
        tmp = list(map(int, input().split()))
        res = [tmp[i:i+3] for i in range(0, 16, 3)]
        cnt = 0
        
        dfs(0)
        answers.append(cnt)
        
    print(*answers)