import sys 

input = sys.stdin.readline

clas = int(input())
student = list(map(int,input().strip().split()))

B, C = map(int,input().split())

count = 0
for i in range(len(student)):
    
    student[i] -= B
    count+=1
    if student[i] <= 0:
        continue
    bu = student[i] // C 
    if student[i] % C !=0: 
        bu+=1
    
    count+=bu     

print(count)
        


