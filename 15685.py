import sys 

input = sys.stdin.readline

N = int(input().strip())

array = [[0]*101 for _ in range(101)]

curves = [list(map(int,input().strip().split())) for _ in range(N)]

dx = [1,0,-1,0]
dy = [0,-1,0,1]

def check(array):
    answer = 0
  
    for l in range(100):
        
        for j in range(100):
            sum=0
            sum +=array[l][j]
            sum +=array[l+1][j]
            sum +=array[l][j+1]
            sum +=array[l+1][j+1]
            if sum == 4:
                answer+=1
    return answer

for i in range(len(curves)):
    curve = curves[i]
    time = curve[3]
    
    end = [curve[1]+dy[curve[2]],curve[0]+dx[curve[2]]]
    array[curve[1]][curve[0]]=1
    array[curve[1]+dy[curve[2]]][curve[0]+dx[curve[2]]]=1
    direction_list = [(curve[2]+2)%4]
    
    while time:
        new_direction_list = direction_list[:]
        
        for k in range(len(direction_list) - 1, -1, -1):
            end = [end[0]+dy[(direction_list[k]-1)%4],end[1]+dx[(direction_list[k]-1)%4]]
            
            array[end[0]][end[1]] =1
            new_direction_list.append(((direction_list[k]-1)%4+2)%4)
            
            
           
        direction_list = new_direction_list
        
        time-=1
    
answer = check(array)
print(answer)
