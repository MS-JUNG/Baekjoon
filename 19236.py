# import sys 
# from collections import defaultdict
# sys.setrecursionlimit(3000)

# def move_fish(direction, index):
#     x, y = index
#     if direction == 1:
#         index = [x, y - 1]
#     elif direction == 2:
#         index = [x - 1, y - 1]
#     elif direction == 3:
#         index = [x - 1, y]
#     elif direction == 4:
#         index = [x - 1, y + 1]
#     elif direction == 5:
#         index = [x, y + 1]
#     elif direction == 6:
#         index = [x + 1, y + 1]
#     elif direction == 7:
#         index = [x + 1, y]
#     elif direction == 8:
#         index = [x + 1, y - 1]
#     return index

# def possible(direction,index,fish):
 
#     for i in range(8):
#         new_index = move_fish(direction,index)
#         new_direction = direction
#         x,y = new_index[0],new_index[1]
#         if (x<0) or (y<0) or (x>3) or (y>3) or (fish[x][y] == -1):  
           
#             direction = (direction+1)%9
#             if direction == 0:
#                 direction+=1
#             continue
         
           
#         else:
#             return new_index,new_direction
    
# def find_fish(matrix, target):
#     for i in range(len(matrix)):
#         for j in range(len(matrix[i])):
#             if matrix[i][j] == target:
#                 return [i, j]

# input = sys.stdin.readline 
# dire = {}
# fish = []

# for i in range(4):
    
#     ka = list(map(int, input().split()))
#     fish.append(ka)

# for i in range(4):
#     for j in range(4):
#         dire[fish[i][j]] = fish[i][j+1]
#         fish[i].pop(j+1)
        

# dire[-1] = dire[fish[0][0]]
# score = 0
# score += fish[0][0]
# shark_dire = dire[fish[0][0]]
# del dire[fish[0][0]]
# fish[0][0] = -1
# total = []

# breakpoint()

# def move_shark(fish,dire):
#     x,y = find_fish(fish,-1)
#     global score
    
#     # if x < 0 or y < 0 or x >= 4 or y >= 4:
#     #     total.append(score)
#     #     return 
    
#     # else:
#     for i in range(1,17):
#         if i not in dire.keys():
#             continue
#         else:
#             direction = dire[i] 
#             index = find_fish(fish,i)
#             new_index,new_direction = possible(direction,index ,fish)
#             dire[i] = new_direction 
        
#             current_fish = fish[index[0]][index[1]]
#             fish[index[0]][index[1]] = fish[new_index[0]][new_index[1]]
#             fish[new_index[0]][new_index[1]] = current_fish
#         # print(dire[-1])
        
    
#     while True:
#         print([x,y])
#         index = move_fish(dire[-1],[x,y])
#         new_x,new_y = index
#         if new_x < 0 or new_y < 0 or new_x >= 4 or new_y >= 4:
#             total.append(score)
#             break
#         else:

#             if fish[new_x][new_y] in dire.keys():
#                 dire[-1] = dire[fish[new_x][new_y]]
#                 score += fish[new_x][new_y]
#                 del dire[fish[new_x][new_y]]
#                 fish[new_x][new_y] = -1
#                 fish[x][y] = 0
#                 move_shark(fish,dire) 
#             else:
#                 pass
            
#             # print(dire)
# move_shark(fish,dire)
# print(total)
# print(fish)


import sys; input = sys.stdin.readline
import copy

# 물고기 좌표 찾는 함수
def find_fish(graph, fish):
    for i in range(N):
        for j in range(N):
            if graph[i][j][0] == fish:
                return (i, j)

# 모든 물고기 이동시키는 함수
def move_fish(x_shark, y_shark, graph):
    # 번호가 낮은 물고기부터 순차 이동
    for fish in range(1, 17):
        # 물고기 좌표 찾기
        position = find_fish(graph, fish)
        # 해당 물고기가 살아있는 경우
        if position:
            x_fish, y_fish = position[0], position[1] # 좌표 리턴받기
            direction = graph[x_fish][y_fish][1]
            # 반시계 방향으로 45도씩 최대 360도(1바퀴)까지 회전
            for _ in range(len(d)):
                # 해당 방향으로 진행
                nx_fish = x_fish + d[direction][0]
                ny_fish = y_fish + d[direction][1]
                # 맵 내부 위치한 경우
                if 0 <= nx_fish < N and 0 <= ny_fish < N:
                    # 진행할 곳에 상어가 없는 경우
                    if not (nx_fish == x_shark and ny_fish == y_shark):
                        # 해당 방향을 진행방향으로 확정
                        graph[x_fish][y_fish][1] = direction
                        # 물고기 간 위치 변경
                        graph[nx_fish][ny_fish], graph[x_fish][y_fish] = graph[x_fish][y_fish], graph[nx_fish][ny_fish]
                        break # 진행방향이 확정되었기 때문에 진행 방향을 더 이상 바꿀 필요 없음
                direction = (direction + 1) % len(d)

# 상어의 이동가능한 좌표 찾는 함수
def get_movable_position(x_shark, y_shark, graph):
    direction = graph[x_shark][y_shark][1] # 상어 진행방향
    position = []
    # 최대 (맵 크기 -1)까지 이동 가능
    for _ in range(N-1):
        # 진행방향으로 전진
        x_shark += d[direction][0]
        y_shark += d[direction][1]
        # 진행 후 맵 내부에 위치해 있으며 물고기가 존재하는 경우
        if 0 <= x_shark < N and 0 <= y_shark < N and graph[x_shark][y_shark][0] != -1:
            position.append((x_shark, y_shark))
    return position

# 물고기를 모두 먹을 때까지 물고기와 상어를 이동시키는 재귀함수
def dfs(x_shark, y_shark, eat, graph):
    global answer
    graph = copy.deepcopy(graph)
    # 상어가 해당 물고기 잡아먹음
    eat += graph[x_shark][y_shark][0]
    graph[x_shark][y_shark][0] = -1 # 해당 위치 물고기 잡아먹힘 표시
    move_fish(x_shark, y_shark, graph) # 모든 물고기 이동
    # 상어의 이동가능한 좌표(=물고기 위치) 리턴받기
    position = get_movable_position(x_shark, y_shark, graph)

    # 이동가능한 좌표가 남은 경우
    if position:
        for nx_shark, ny_shark in position:
            dfs(nx_shark, ny_shark, eat, graph)
    else:
        answer = max(answer, eat)
        return

N = 4
graph = [[None]*N for _ in range(N)]
for i in range(N):
    data = list(map(int, input().split()))
    for j in range(N):
        # 물고기 번호, 방향 정보 저장
        # 방향 정보 값에 1을 뺀 이유: 진행방향을 저장한 리스트(d)의 값이 인덱스 0부터 시작하기 떄문
        graph[i][j] = [data[2*j], data[2*j+1]-1]

# 진행방향: 상, 좌상, 좌, 좌하, 하, 우하, 우, 우상
d = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
# (0, 0)에서 시작
x_shark = y_shark = 0
answer = 0
dfs(x_shark, y_shark, 0, graph)
print(answer)