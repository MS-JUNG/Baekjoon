import sys 

input = sys.stdin.readline
N = int(input().strip())

food = list(map(int,input().split(' ')))

array = [0]*N

array[0] = food[0]
array[1] = max(food[0],food[1])
array[2] = food[0] + food[2]

for i in range(3,N):
    array[i] = max(array[i-2] + food[i],array[i-1])
print(array)


# n = int(input())
# array = list(map(int,input().split()))
# d=[0]*100

# d[0]=array[0]
# d[1]=max(array[0],array[1])
# for i in range(2,n):
#     d[i] = max(d[i-1],d[i-2]+array[i])
    
# # print(d[n-1])
# print(d)