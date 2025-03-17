import sys 
import os 
input = sys.stdin.readline

N = list(input().strip())

N = [int(k) for k in N]

length = len(N)

pos = length-1
for i in range(pos):
    if N[length-i-1] >  N[length-i-2]:
        pivot = length-i-2
        break

for j in range(pivot+1, length):
    
    if N[j] > N[pivot]:
        pass
    else: 
        pos = j-1    
        
        break   

N[pos],N[pivot] = N[pivot],N[pos]
N[pivot+1:] = reversed(N[pivot+1:])

number_str = ''.join(map(str, N))
result = int(number_str)

print(result)
