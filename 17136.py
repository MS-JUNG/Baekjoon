import sys 

input = sys.stdin.readline

array = [list(map(int,input().split())) for _ in range(10)]
length = [1,2,3,4,5]
count = [5,5,5,5,5]

def check(array,i,j,length):
    
    for a in range(length):
        for b in range(length):
            if array[i+a][j+b] == 1:
                pass
            else:
                return False
    
    return length
max_ls= []
score = 0
def find(p):
    global score
    
    for i in range(10):
        for j in range(10):
            if array[i][j] == 1:
                for k in range(5):
                    leng = length[k]
                    if count[k] != 0:
                        
                        if check(array,i,j,leng):
                            count[k] -= 1
                            array[i:i+leng][j:j+leng] = 0
            
                            find(p+1)
                            count[k] +=1
                            array[i:i+leng][j:j+leng] = 1
                        
                    else:
                        pass
            else:
                max_ls.append(score)
                
                    
            
            
    
    
find()
print(min(max_ls))



def promise(a1, a2, b1, b2): #유망 조건
    for i in range(a1, a2+1):
        for j in range(b1, b2+1):
            if not paper[i][j]:
                return False
    return True

def attach(a1, a2, b1, b2, w): # 색종이 붙이기/떼기
    for i in range(a1, a2+1):
        for j in range(b1, b2+1):
            paper[i][j] = w

def glue(p):
    global result
    for y in range(10):
        for x in range(10):
            if paper[y][x]:
                for c in range(5):
                    ny, nx = y + c, x + c
                    if confetti[c] and ny < 10 and nx < 10 : # 색종이가 남았고 범위안에 있으면
                        if promise(y, ny, x, nx): 
                            attach(y, ny, x, nx, 0)
                            confetti[c] -= 1
                            glue(p+1) # 백트래킹
                            confetti[c] += 1
                            attach(y, ny, x, nx, 1)
                return
    result = min(result, p)

import sys
paper = [list(map(int, sys.stdin.readline().split())) for _ in range(10)]
confetti = [5, 5, 5, 5, 5]
result = 26
glue(0)
if result == 26:
    print(-1)
else:
    print(result)
