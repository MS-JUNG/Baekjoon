import sys 

input = sys.stdin.readline

N,M,K = map(int,input().strip().split())

array = [list(map(int,input().strip().split())) for _ in range(N)]

tree = []

food = [[5]*N for _ in range(N)]


for i in range(M):
    tree.append(list(map(int,input().strip().split())))

for i in tree:
    i[0]-=1
    i[1]-=1
    

finish = 0


dx = [0,0,1,1,1,-1,-1,-1]
dy = [1,-1,0,1,-1,0,1,-1]
while finish != K:
    dead = []
    finish+=1 
    tree.sort(key=lambda x: x[2])
    propagate = []
    for t in tree[:]:
        if food[t[0]][t[1]] - t[2] < 0:
            dead.append(t)
            tree.remove(t)
        else:
            t[2] +=1
            food[t[0]][t[1]] -= t[2]
            if t[2] %5 == 0:
                propagate.append(t)
            
    
    for j in dead:
        food[j[0]][j[1]] += j[2]//2
    for k in propagate:
        for l in  range(8):
            nx = k[0] + dx[l]
            ny = k[1] + dy[l]
            if 0<=nx<N and 0<=ny<N: 
                tree.append([nx,ny,1])
    result = [[0]*len(array[0]) for _ in range(len(array))]
    for i in range(len(array)):
        for j in range(len(array[i])):
            result[i][j] = array[i][j] + food[i][j]
            
    food=result

print(len(tree))

                

    

    
    