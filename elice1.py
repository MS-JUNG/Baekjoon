def next_permutation(num):
    numbers = list(num) 
    length = len(numbers)
    
    i = length - 2

    while i >= 0 and numbers[i] >= numbers[i + 1]:
        i -= 1

    if i == -1:
        return None  

    j = length - 1
    while numbers[j] <= numbers[i]:
        j -= 1


    numbers[i], numbers[j] = numbers[j], numbers[i]


    numbers[i + 1:] = reversed(numbers[i + 1:])

    return int(''.join(numbers)) 


N = int(input().strip())
next_number = next_permutation(str(N))
print(next_number)