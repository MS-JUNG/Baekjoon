

N = int(input())

target = list(map(int,input().split()))
material = [list(map(int,input().split())) for _ in range(N)]
answer =[]

def recur(idx,mete, present,price):
    global answer 
    global target 
    if present[0] >= target[0] and present[1] >= target[1] and present[2] >= target[2] and present[3] >= target[3]:
        
        answer.append([mete,price])
        return
    
    if idx == N:
        return
    
    present_past = present.copy()
    present_new = [present[i] + material[idx][i] for i in range(0,4)]
    price_past = price
    price_new = price + material[idx][4]
    
    recur(idx+1, mete +[idx+1],present_new,price_new )
    recur(idx+1,mete, present_past,price_past)


recur(0,[],[0,0,0,0],0)

if len(answer)==0:
    print(-1)
else:
    answer.sort(key = lambda x :(x[1],x[0]))
    print(answer[0][1])
    print(" ".join(map(str,answer[0][0])))
    
    
