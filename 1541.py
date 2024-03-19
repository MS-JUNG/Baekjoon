value = str(input())
split = value.split('-')

answer = 0
x = sum(map(int, (split[0].split('+'))))

answer += x

for x in split[1:]: 
    x = sum(map(int, (x.split('+'))))
    answer -= x
print(answer)