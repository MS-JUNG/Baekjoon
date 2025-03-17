import sys 

input = sys.stdin.readline
N,M,K = map(int, input().strip().split())
number = list(map(int, input().strip().split()))
max = sorted(number,reverse=True)


result = 0
repeat = M//(K+1)

value = repeat * (K*max[0]+max[1])
seperate = M%(K+1)

value2 = max[0] * seperate 
breakpoint()

print(value+value2)