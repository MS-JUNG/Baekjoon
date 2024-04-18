import sys 

input = sys.stdin.readline
N, M = map(int,input().strip().split())
board = [list(map(int,input().strip().split())) for _ in range(N)]
def rotate_90(matrix):
    return [list(reversed(col)) for col in zip(*matrix)]
def rotate_n_times(matrix, n):
    result = matrix
    for _ in range(n):
        result = rotate_90(result)
    return result
board = board
board_90 = rotate_n_times(board,1)
board_180 = rotate_n_times(board,2)
board_270 = rotate_n_times(board,3)

max_list=[]

def check_1(board,dir):
    if dir == 1 or dir == 3:
       row, col  = M, N
    else:
        row, col = N,M
    max = 0
    for j in range(row):
        for i in range(col-3):
            
            value = board[j][i] + board[j][i+1] + board[j][i+2] + board[j][i+3]
            if value >= max:
                    max = value
    return max 
def check_2(board,dir):
    if dir == 1 or dir == 3:
       row, col  = M, N
    else:
        row, col = N,M
    max = 0 
    for j in range(row-1):
        for i in range(col-1):
            value = board[j][i] + board[j][i+1] + board[j+1][i] + board[j+1][i+1]
            if value > max:
                max = value
    return max 
def check_3(board,dir):
    if dir == 1 or dir == 3:
       row, col  = M, N
    else:
        row, col = N,M
    max = 0 
    for j in range(row-1):
        for i in range(col-2):
            value = board[j][i] + board[j][i+1] + board[j][i+2] + board[j+1][i+1]
            if value > max:
                max = value
    return max
def check_4(board,dir):
    if dir == 1 or dir == 3:
       row, col  = M, N
    else:
        row, col = N,M
    max = 0 
    for j in range(row-1):
        for i in range(col-2):
            value = board[j][i] + board[j][i+1] + board[j][i+2] + board[j+1][i]
            value_2 = board[j][i] + board[j][i+1] + board[j][i+2] + board[j+1][i+2]
            if value > max:
                max = value
            if value_2 > max:
                max = value_2    
    return max

def check_5(board,dir): 
    max = 0
    if dir == 1 or dir == 3:
       row, col  = M, N
    else:
        row, col = N,M
    for j in range(row-1):
        for i in range(col-2):
            value = board[j][i] + board[j][i+1] + board[j+1][i+1] + board[j+1][i+2]
            value_2 = board[j][i+1] + board[j][i+2] + board[j+1][i] + board[j+1][i+1]
            if value > max:
                max = value
            if value_2 > max:
                max = value_2
    return max

max_list = [check_1(board,0),check_1(board_90,1),check_2(board,0)
            ,check_3(board,0),check_3(board_90,1),check_3(board_180,2),check_3(board_270,3)
            ,check_4(board,0),check_4(board_90,1),check_4(board_180,2),check_4(board_270,3)
            ,check_5(board,0),check_5(board_90,1),check_5(board_180,2),check_5(board_270,3)]

print(max(max_list))
