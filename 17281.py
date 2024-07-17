import sys 
import itertools
input = sys.stdin.readline
N = int(input())
conditions = [list(map(int, input().split()))for _ in range(N)]
bat = [2,3,4,5,6,7,8,9]
max_score = -1000
for perm in list(itertools.permutations(bat)):
    score = 0
    batter_ord = list(perm[:3]) + [1] + list(perm[3:])
    order = 0 
    for i in range(N):
        out = 0
        ru = [0,0,0,0,0,0,0]
        while out != 3:
            hit = conditions[i][batter_ord[order]-1]
            if hit == 0:
                out+=1
                
            else: 
                temp = ru[:3]
                ru[hit:hit+3] = temp
                ru[hit-1] = 1
                    
            score += sum(ru[3:])     
            ru[3:] = [0,0,0,0]
            order +=1
            if order == 9:
                order = 0
    if score > max_score:
        max_score = score
        
print(max_score)
            
            