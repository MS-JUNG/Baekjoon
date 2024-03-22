import sys

input = sys.stdin.readline

count = int(input().strip())
tree_list = [int(input()) for _ in range(count)]
tree_between = []

for i in range(len(tree_list)-1):
    tree_between.append(tree_list[i+1]-tree_list[i])




min_v = min(tree_between)
for k in range(len(tree_between)):
        if tree_between[k] % min_v == 0:
            
            pass
        else:
            iter = min_v
            for j in range(1,iter//2+1):
                if (iter % j == 0) and (tree_between[k] % j == 0):          
                    min_v = j
      
result = 0
for i in range(len(tree_between)):
    result += ((tree_between[i] // min_v ) -1)

print(result)
    
    

            
            
    