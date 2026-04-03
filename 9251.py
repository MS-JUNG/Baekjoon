first = list(input())
second = list(input())


mem = [[0 for _ in range(len(second))]  for _ in range(len(first))]

for i in range(len(first)):
    if first[i] == second[0]:
        mem[i][0] = 1
    else:
        mem[i][0] = mem[i-1][0]

for j in range(len(second)):
    if first[0] == second[j]:
        mem[0][j] = 1
    else:
        mem[0][j] = mem[0][j-1]

for i in range(1,len(first)):
    for j in range(1,len(second)):
        
        if first[i] == second[j]:
            mem[i][j] =  mem[i-1][j-1] +1 
        else:
            
            mem[i][j] = max(mem[i-1][j],mem[i][j-1])

print(mem[len(first)-1][len(second)-1])