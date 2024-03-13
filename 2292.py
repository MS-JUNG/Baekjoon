room = int(input())


line  = (room-2)//6 
real_line = 0
n = 0

while line >= 0:
    line -= n
    real_line += 1 
    n += 1

if room == 1:
    real_line = 1


    
print(real_line)