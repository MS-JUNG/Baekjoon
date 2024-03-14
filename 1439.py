word = list(str(input()))



count = 0

while len(word) != 0:
    letter = word.pop()
    if len(word) == 0:
        break
    
    if letter != word[-1]:
        count += 1 
            
    else:
        pass
if count % 2 == 0:
    count = count //2
else:
    count = count // 2 + 1
    
print(count)


    



