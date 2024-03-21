import sys 


input = sys.stdin.readline
N = list(str(input().strip()))

score = 0
list = [int(x) for x in N ] 

forward = sum(list[:len(list)//2])
backward = sum(list[len(list)//2:])

    
    
if forward == backward:
    print('LUCKY')
else:
    print('READY')