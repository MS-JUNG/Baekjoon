N = int(input())

total = list(map(int, input().split()))

# 각 위치의 가장 긴 증가하는 부분 수열의 길이를 저장할 배열, 모든 값은 최소 1이어야 함
mem = [1] * N

for i in range(1, N):
    for j in range(i):
        if total[i] > total[j]:
            mem[i] = max(mem[j] + 1, mem[i])

print(max(mem))