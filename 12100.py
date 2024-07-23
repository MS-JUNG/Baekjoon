import sys 

input = sys.stdin.readline

N = int(input().strip())
array = [list(map(int,input().strip().split())) for _ in range(N)]


def next(map,cnt):
    
    temp = map 
    
    for i in range(4):
        
        cnt+=1
        next(temp,cnt)
        
    
    
    
    
    
    if cnt == 5:
       max_v = 0
       for i in map:
           if max(i) > max_v:
               max_v = max(i)
           
       return max_v




for i






# for a in range(4):
#     for b in range(4):
#         for c in range(4):
#             for d in range(4):
#                 for e in range(4):
                    