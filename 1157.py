

word = input()


word = word.lower()

word_1 = list(word)
alphabet_list = list(set(word_1))
value = 0 
list_c = []
for i in range(len(alphabet_list)):
    max_value = word.count(alphabet_list[i])
    if value < max_value:
        value = max_value
        list_c = []
        list_c.append(alphabet_list[i])
    elif value == max_value:
        value = max_value
        list_c.append(alphabet_list[i])
    else:
        pass   

if len(list_c) > 1:
    print('?')
else:
    print(list_c[0].upper())
        