import sys 

input = sys.stdin.readline
R,C,M = map(int,input().strip().split())

# x,y,속력,방향,크기
dx = ['empty',-1,1,0,0]
dy = ['empty',0,0,1,-1]
shark = [list(map(int,input().strip().split())) for _ in range(M)]
for l in shark:
    ## 인덱스 0부터로 맞춰주기 
    l[0]-=1
    l[1]-=1

result = 0
for i in range(C):
    array = [[[] for _ in range(C)] for _ in range(R)]
    
    shark.sort()
    print(shark)
    for s in range(len(shark)):
        
        if shark[s][1] == i:
            
            # shark를 행이 커지는 순으로 sorting해놓았기때문에 열이 일치하는 가장 첫번째 상어를 잡으면 그게 가장 가까운 상어
            result+=shark[s][4]
            ka = shark.pop(s)
            
            break
    breakpoint()
    for k in range(len(shark)):
        x = shark[k][0]
        y = shark[k][1]
        d  = shark[k][3]
        speed = shark[k][2]
        ## 상어를 속력이 0이 될떄까지 계속해서 1씩 빼면서 최종위치를 구함
        while speed>0:
            # print(speed)
            nx = x+dx[d]
            ny = y+dy[d]
            
            ### 만약 상어가 밖으로 갈려하면 방향만 바꿔주고 speed는 빼지않고 다음 싸이클로 넘어감
            if nx<0 or nx>=R or ny<0 or ny>=C:
                if d in [1,3]:
                    d+=1
                
                elif d in [2,4]:
                    d-=1
                continue
            else:
                x = nx
                y = ny
                speed-=1
        shark[k][3]=d
        
        ### 빈 배열에 이동이 끝난 상어를 넣음 
        array[x][y].append(shark[k][2:])

    shark = []
    
    ### 새롭게 이동이 끝난 상어를 array에 남김 이때 겹치는 상어는 큰것만 남겨야댐 
    for row in range(R):
        for col in range(C):
            
            if len(array[row][col])>=2:
                
                # 몸무게 순으로 정렬해서 큰것만 상어 리스트에 넣음 
                array[row][col].sort(key = lambda x:x[2], reverse=True)
                
                shark.append([row,col]+array[row][col][0])
            elif len(array[row][col])==1:
                
                # 1개남은건 그대로 상어리스트에 넣음 
                shark.append([row,col]+array[row][col][0])
                
            else:
                pass
     
    

print(result)