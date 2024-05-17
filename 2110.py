import sys 
input = sys.stdin.readline

num_houses, num_routers = map(int,input().strip().split())

houses = [ int(input()) for _ in range(num_houses)]

houses.sort()

def can_place_routers(distance):
    
    count = 1 
    next_router = houses[0]
    
    for i in range(1,num_houses):
        
        if houses[i] - next_router >= distance:
            count +=1 
            next_router = houses[i]
        
        if  count > num_routers:
            return True 
    
    return False
        
        

start = 1 
end = houses[-1] - houses[0]

result = 0


while start <= end:
    mid = (start+end)//2
    if can_place_routers(mid):
        result = mid
        start = mid + 1
    
    else:
        end = mid - 1
        
print(result)
