import sys 
import itertools

input = sys.stdin.readline

N,M,D = map(int,input().split())

array = [list(map(int,input().split())) for _ in range(N)]
total_enemy=0
combination = itertools.combinations(range(M),3)


for j in array:
    total_enemy += sum(j)
    


for i in range(N):
    for i in range(3):
        
        
        
        
    
    
    
    
    
    
    
    enemy = sum(array.pop())
    array.insert(0,[0]*5)
    total_enemy-=enemy 


