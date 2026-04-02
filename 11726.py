n = int(input())
ansList = [0]*n
ansList[0] = 1

if n >= 2:
    ansList[1] = 2
    for i in range(2, n):
        ansList[i] = ansList[i-1] + ansList[i-2]

print(ansList[n-1] % 10007)