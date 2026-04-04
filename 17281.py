import sys
from itertools import permutations

input = sys.stdin.readline

N = int(input().strip())
innings = [list(map(int, input().split())) for _ in range(N)]

players = [2, 3, 4, 5, 6, 7, 8, 9]
max_score = 0

def simulate(order):
    score = 0
    hitter_idx = 0

    for inning in range(N):
        out = 0
        b1, b2, b3 = 0, 0, 0

        while out < 3:
            player = order[hitter_idx]
            result = innings[inning][player - 1]

            if result == 0:
                out += 1

            elif result == 1:
                score += b3
                b1, b2, b3 = 1, b1, b2

            elif result == 2:
                score += b2 + b3
                b1, b2, b3 = 0, 1, b1

            elif result == 3:
                score += b1 + b2 + b3
                b1, b2, b3 = 0, 0, 1

            else:  # result == 4
                score += b1 + b2 + b3 + 1
                b1, b2, b3 = 0, 0, 0

            hitter_idx = (hitter_idx + 1) % 9

    return score

for perm in permutations(players):
    order = list(perm[:3]) + [1] + list(perm[3:])
    max_score = max(max_score, simulate(order))

print(max_score)