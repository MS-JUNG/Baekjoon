import sys 
from collections import defaultdict

input = sys.stdin.readline 
N,M,x,y,K = map(int,input().strip().split())

array = [list(map(int,input().strip().split())) for _ in range(N)]
1

command = list(map(int,input().strip().split()))

# 각 면에 어떤 값이 담길 지 저장히는 딕셔너리
number = defaultdict(int)
#바닥이 key 일때 굴려 지는 방향에 따라 바닥의 위치를 지정하는 딕셔너리 리스트의 0번 요소는 상단 1번 부터 4번 요소까지 차례로 동서북남 의 순서 
dicts = {6:[1,3,4,5,2],1:[6,3,4,2,5],3:[4,6,1,2,5],4:[3,1,6,2,5],2:[5,3,4,6,1],5:[2,3,4,1,6]}
for i in range(1,7):
    number[i] = 0


bottom = 6
pos = [x,y]

# 방향 전환 0번 인덱스는 필요없어서 막넣음
dy = [100,1,-1,0,0]
dx = [100,0,0,-1,1]

for i in range(K):
    # 다음 위치 
    nx = pos[0]+dx[command[i]]
    ny = pos[1]+dy[command[i]]
    
    # 다음 위치 가능여부 확인 
    if 0<=nx<N and 0<=ny<M:
        pos = [nx,ny]
        # 다음 바닥 위치 지정 
        bottom = dicts[bottom][command[i]]
        
        if array[nx][ny]==0:
            array[nx][ny] = number[bottom]
            
        else:
            number[bottom] = array[nx][ny]
            array[nx][ny]=0
            
        #상단 위치 출력 
        print(number[dicts[bottom][0]])

    else:
        pass

breakpoint()