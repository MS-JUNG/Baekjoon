import sys  
input = sys.stdin.readline
number = int(input().strip())

d = [0]*30000

d[1]=0
for i in range(2,number+1):
    if i%5 == 0:
        d[i]=d[i//5]+1
    elif i%3 == 0:
        d[i]=d[i//3]+1
    elif i%3 == 0:
        d[i]=d[i//2]+1
    else:
        d[i] = d[i-1]+1
        

print(d[number])
    