import sys
input = sys.stdin.readline

N = int(input().strip())
expr = input().strip()

nums = []
ops = []

for i, ch in enumerate(expr):
    if i % 2 == 0:
        nums.append(int(ch))
    else:
        ops.append(ch)

def calc(a, op, b):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    else:
        return a * b

ans = -float('inf')
m = len(ops)

def dfs(idx, cur):
    global ans

    if idx == m:
        ans = max(ans, cur)
        return

    # 1. 현재 연산을 바로 수행
    dfs(idx + 1, calc(cur, ops[idx], nums[idx + 1]))

    # 2. 다음 연산을 괄호로 묶을 수 있으면 묶어서 수행
    if idx + 1 < m:
        bracket = calc(nums[idx + 1], ops[idx + 1], nums[idx + 2])
        dfs(idx + 2, calc(cur, ops[idx], bracket))

dfs(0, nums[0])
print(ans)