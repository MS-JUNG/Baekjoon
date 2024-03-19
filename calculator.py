import sys
# input = sys.stdin.readline
word = list(input())


value_list = []
cal_list = []
value = ''  

for i in range(len(word)):
    
    if i == len(word)-1:
      value += word[i]
      value_list.append(value)
    

    if word[i] == '-':
        cal_list.append(word[i])
        value_list.append(value)
        value =''
    elif word[i] == '+':
        cal_list.append(word[i])
        value_list.append(value)
        value =''
   
    else: 
        value += word[i]
        # print(value)


def calculator(value_list, cal_list):
    value = int(value_list[0])
    value_list = value_list[1:]
    for i in range(len(value_list)):
        if cal_list[i] == '+':
            value += int(value_list[i] )
        else:
            value -= int(value_list[i] )
    return value 


        
        
print(value_list)
print(cal_list)


print(calculator(value_list, cal_list))