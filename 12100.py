import sys 

import copy 
input = sys.stdin.readline

N = int(input())

board = [list(map(int,input().strip().split())) for _ in range(N)]



def left(array):
    
    for i in range(N):
        pointer = 0 
        for j in range(1,N):
            if array[i][j] != 0:
                tmp = array[i][j]
                array[i][j] = 0

                if array[i][pointer] == tmp:
                    array[i][pointer] = tmp*2
                    pointer+=1 
                elif array[i][pointer] == 0:
                    array[i][pointer] = tmp
                else:
                    pointer+=1
                    array[i][pointer] = tmp
                    
    return array

def right(array):
     
    for i in range(N):
        pointer = N-1
        for j in range(N-1,-1,-1):
            
            if array[i][j] != 0:
                tmp = array[i][j]
                array[i][j] = 0

                if array[i][pointer] == tmp:
                    array[i][pointer] = tmp*2
                    pointer-=1 
                elif array[i][pointer] == 0:
                    array[i][pointer] = tmp
                else:
                    pointer-=1
                    array[i][pointer] = tmp
                    
    return array

def up(array):
    
    for i in range(N):
        pointer = 0 
        for j in range(1,N):
            if array[j][i] != 0:
                tmp = array[j][i]
                array[j][i] = 0

                if array[pointer][i] == tmp:
                    array[pointer][i] = tmp*2
                    pointer+=1 
                elif array[pointer][i] == 0:
                    array[pointer][i] = tmp
                else:
                    pointer+=1
                    array[pointer][i] = tmp
                    
    return array

def down(array):
    
    for i in range(N):
        pointer = N-1
        for j in range(N-1,-1,-1):
            if array[j][i] != 0:
                tmp = array[j][i]
                array[j][i] = 0 

                if array[pointer][i] == tmp:
                    array[pointer][i] = tmp*2
                    pointer-=1 
                elif array[pointer][i] == 0:
                    array[pointer][i] = tmp
                else:
                    pointer-=1
                    array[pointer][i] = tmp
                    
    
    return array





max_v = 0
def move(array,cnt):
    global max_v
    
    if cnt == 5:
        
        for k in array:
            if max(k) > max_v:
                max_v =max(k)
        return
    else:
        cnt+=1
        move(up(copy.deepcopy(array)),cnt)
        move(down(copy.deepcopy(array)),cnt)
        move(left(copy.deepcopy(array)),cnt)
        move(right(copy.deepcopy(array)),cnt)
        

move(board,0)

print(max_v)