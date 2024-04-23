import sys
import itertools

input = sys.stdin.readline

N = int(input().strip())

score_map = [ list(map(int, input().strip().split())) for _ in range(N)]
team_num = list(range(N))
team = list(itertools.combinations(team_num,N//2))
# for i in range(len(team)):
    
mins = []

for i in range(len(team)//2+1):
    team_a = list(team[i]) 
    team_b = []
    
    
    for i in range(N):
        if i not in team_a:
            team_b.append(i)
            
    score_a = 0
    score_b = 0
    a_list = list(itertools.combinations(team_a,2))
    b_list= list(itertools.combinations(team_b,2))
    
    for i in a_list:
        score_a += score_map[i[0]][i[1]]
        score_a += score_map[i[1]][i[0]]
    for j in b_list:
        score_b += score_map[j[0]][j[1]]
        score_b += score_map[j[1]][j[0]]
    if abs(score_a - score_b) == 0:
        mins = [0]
        break    
    mins.append(abs(score_a -score_b))
   
    
print(min(mins))
    
