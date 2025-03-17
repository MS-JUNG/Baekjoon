import sys 

input = sys.stdin.readline
N,M = map(int, input().split())
map = [list(map(int, input().strip().split())) for _ in range(N)]

maxs = []
for i in map:
    maxs.append(min(i))
    
print(max(maxs))