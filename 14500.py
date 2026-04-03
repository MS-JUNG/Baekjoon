N, M = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range (N)]

v= [[0] * M for _ in range (N)] # dfs 방문 표시 배열

# 각 행에서 최대값을 찾은 뒤, 그 중 전체 배열의 최댓값을 찾음
mx = max(map(max, arr))

dx = [-1,1,0,0]
dy = [0,0,-1,1]

def dfs(n, temp, lst) :
    global ans

    # 가지치기
    if temp + (4-n) * mx <= ans : # 나머지 블럭이 모두 최댓값이어도 현재 ans 값보다 작다면 dfs 순회 정지
        return

    # 종료 조건
    if n == 4 :
        ans = max(temp, ans)
        return
    
    # 재귀 함수 호출 (자기 위치에서 뻗어나가기, 백트래킹)
    for cx, cy in lst :
        for i in range (4) :
            nx, ny = cx + dx[i], cy + dy[i]
            # 범위, 방문 검사
            if 0 <= nx < N and 0<= ny < M and v[nx][ny] == 0 :
                v[nx][ny] = 1
                dfs(n+1, temp + arr[nx][ny], lst + [(nx, ny)])
                v[nx][ny] = 0 # 방문표시 해제로 백트래킹

ans = 0
for i in range (N) :
    for j in range (M) :
        v[i][j] = 1
        dfs(1, arr[i][j], [(i,j)])

print(ans)