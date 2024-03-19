count = int(input())

paper = [[0 for _ in range(100)] for _ in range(100)]

print(paper)
for i in range(count):
    a, b = map(int, input().split())
    for j in range(a,a+10):
        
        for k in range(b, b+10):
            if j>=100 | k>=100:
                break
    
            paper[j][k] = 1
total = 0

for i in paper:
    total += sum(i)

print(total)



## 틀린 방법  ->> 교집합을 여러번 빼서 중복햇 뺴는 문제 발생 

# count = int(input())
# square = []
# for i in range(count):
#     a, b = map(int, input().split())
#     square.append([a, b])

# first = 100 * count
# for i in range(count):
#     sq = square.pop()

#     for i in range(len(square)):

#         if ((abs(sq[0] - square[i][0]) >= 10) or (abs(sq[1] - square[i][1]) >= 10)):
#             pass
#         else: 

#             cross = (10-abs(sq[0]-square[i][0]))*(10-abs(sq[1]-square[i][1]))
#             first -= cross

         
    
# print(first)


