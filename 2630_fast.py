import sys
input = sys.stdin.readline

n = int(input())
array = [list(map(int, input().split())) for _ in range(n)]

one = 0
zero = 0

def cut(x, y, size):
    global one, zero

    first = array[x][y]
    same = True

    for i in range(x, x + size):
        for j in range(y, y + size):
            if array[i][j] != first:
                half = size // 2
                cut(x, y, half)
                cut(x + half, y, half)
                cut(x, y + half, half)
                cut(x + half, y + half, half)
                return

    if first == 0:
        zero += 1
    else:
        one += 1

cut(0, 0, n)
print(zero)
print(one)