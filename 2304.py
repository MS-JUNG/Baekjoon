N = int(input())

box = []
for i in range(N):
 box.append(list(map(int,input().split())))
 
box.sort()

now = box.pop()
now_x, now_y = now[0], now[1]
while box:
    
    next = box.pop()
    next_x, next_y = next[0], next[1]
    
   
    