N, M = map(int,input().split())

array = [[int(i) for i in input()] for _ in range(N)]
visited = [[0 for _ in range(N)] for _ in range(M)]
move = [[0,1],[1,0],[-1,0],[0,-1]]


    
    
def finding(a,b): #길을 찾아주자
    visited = [[0]* M for _ in range(N)]
    queue = [[a,b]]
    visited[a][b] = 1 # 방문 처리
    while queue:
        y, x = queue.pop(0)
        for dy, dx in move:
            ny, nx = y + dy, x + dx
            if 0 <= ny < N and 0 <= nx < M and visited[ny][nx] == 0 and maze[ny][nx] != 0:
                visited[ny][nx] = visited[y][x] + 1 # 출발지부터 이동한 거리재기
                queue.append([ny,nx])
    return visited[N-1][M-1] #도착점 도착했을 때 거리

import sys
N, M = map(int, sys.stdin.readline().split())
maze = [list(map(int, sys.stdin.readline().strip())) for _ in range(N)]
move = [[1,0],[-1,0],[0,1],[0,-1]]
print(finding(0,0)) #출발 지점

    
    