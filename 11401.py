import sys 

input = sys.stdin.readline

N, K = map(int,input().strip().split())

result = 1
divide = 1
for i in range(K):
    result *= N
    N-=1
    divide *= (i+1)

result /= divide
result = int(result)%1000000007
print(result)