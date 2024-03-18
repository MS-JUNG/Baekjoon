import sys
input = sys.stdin.readline
def plist(first,move):
    return [first[0]+move[0],first[1]+move[1]]
N=int(input())
n_1=int(input())
apple=[list(map(int, input().split())) for _ in range(n_1)]
n_2=int(input())
move=[list(input().split()) for _ in range(n_2)]
move_time=[int(i) for i,j in move]
direction=[[0,1],[1,0],[0,-1],[-1,0]]
snake=[[1,1]]
time=0
dire=0



while True:
    if time in move_time:
        if move[move_time.index(time)][1] == 'D':
            dire+=1
            dire=dire%4 
        else:
            dire-=1 
            dire=dire%4

    new=plist(snake[-1],direction[dire])
    if new[0] >= N+1 or new[0] <= 0 or new[1] >= N+1 or new[1] <=0 or new in snake:
        break
    if new in apple:
        apple.remove(new)
         
    else:
        del snake[0]
    snake.append(new)
    time += 1
    

print(time+1)
    
    
    
    
    
            
    





































