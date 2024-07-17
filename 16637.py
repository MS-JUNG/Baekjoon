import sys 

input = sys.stdin.readline

N = int(input().strip())

cal = list(map(str,input().strip()))



def calculator(pre,pos,digit):
    if digit=='+':
        value = pre + pos
    if digit=='-':
        value = pre - pos
    
    if digit=='*':
        value = pre * pos
    
    return value 

breakpoint()


def dfs(pos,value)



    
    dfs(pos,)


