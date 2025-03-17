


position = list(input())

row = int(position[1])
column = ord(position[0])-ord('a')+1


steps = [(-2,-1),(-1,-2),(1,-2),(2,-1),(2,1),(1,2),(-1,2),(-2,1)]


answer = 0
for i in steps:
    if  (1 <= row+i[0] <=8) and (1 <= column+i[1]<= 8):
        answer+=1

    else:
        pass
        
        
        
    
print(answer)
