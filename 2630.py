import sys 

n = int(sys.stdin.readline())
array = [list(map(int, input().split())) for _ in range(n)]


one = 0
zero = 0

def cut(s,f,N):
    global one, zero
    seq = 0
    
    for i in range(s,s+N):
        for j in range(f,f+N):
            seq += array[i][j]
    if seq == N**2:
    
        one += 1
    elif seq == 0:
        
        zero += 1
    else:
        cut(s,f, N//2)
        cut(s+N//2,f, N//2)
        cut(s,f+N//2, N//2)
        cut(s+N//2,f+N//2, N//2)
    
     
cut(0,0,n)
print(zero)
print(one)