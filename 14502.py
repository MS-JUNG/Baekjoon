import sys
import itertools
import copy
input = sys.stdin.readline



N, M = map(int,input().strip().split())
board = [list(map(int,input().strip().split())) for _ in range(N)]
zero_index = []
virus_index = []
for i in range(N):
    for j in range(M):
        if board[i][j] == 0:
            zero_index.append([i,j])
        elif board[i][j] == 2:
            virus_index.append([i,j])
combinations = list(itertools.combinations(zero_index,3))


try_s = len(combinations)
from collections import deque

def move(i):
    
    
    return [i[0]-1,i[1]], [i[0]+1,i[1]], [i[0],i[1]-1], [i[0],i[1]+1]

def search_max(board_try,virus_index):
    que = deque()

    for i in virus_index:
        que.append(i)
    while que:
        
        recent = que.popleft()
        aa,bb,cc,dd = move(recent)
        
        if (aa[0] >=0) and (aa[0] < N) and  (aa[1] >=0) and (aa[1] < M):
            if board_try[aa[0]][aa[1]] == 0:
                board_try[aa[0]][aa[1]] = 1
                que.append(aa)
            else:
                pass
        if (bb[0] >=0) and (bb[0] < N) and  (bb[1] >=0) and (bb[1] < M):
            if board_try[bb[0]][bb[1]] == 0:
                board_try[bb[0]][bb[1]] = 1
                que.append(bb)
            else:
                pass
                
        if (cc[0] >=0) and (cc[0] < N) and  (cc[1] >=0) and (cc[1] < M):
            if board_try[cc[0]][cc[1]] == 0:
                board_try[cc[0]][cc[1]] = 1
                que.append(cc)
            else:
                pass
        if (dd[0] >=0) and (dd[0] < N) and  (dd[1] >=0) and (dd[1] < M):
            if board_try[dd[0]][dd[1]] == 0:
                board_try[dd[0]][dd[1]] = 1
                que.append(dd)
            else:
                pass
    max = 0
    for i in range(N):
        for j in range(M):
            if board_try[i][j] == 0:
                max+=1
          
            
    
    return max
            
    
max_list = []
try_s = len(combinations)
for i in range(try_s):
    board_try = copy.deepcopy(board)
    board_try[combinations[i][0][0]][combinations[i][0][1]] = 1
    board_try[combinations[i][1][0]][combinations[i][1][1]] = 1
    board_try[combinations[i][2][0]][combinations[i][2][1]] = 1

    max_1 = search_max(board_try,virus_index)

    max_list.append(max_1)

print(max(max_list))



            