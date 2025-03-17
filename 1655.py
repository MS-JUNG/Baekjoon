import sys 
import bisect

def insert_in_sorted_list(sorted_list, value):
    # bisect.insort_left를 사용하여 값을 삽입합니다.
    bisect.insort_left(sorted_list, value)

input = sys.stdin.readline


N = int(input())

array = []
for i in range(N):
    if i == 0:
        array.append(int(input()))
    
        if len(array)%2 == 0:
            print(array[len(array)//2-1])
        else:
            print(array[len(array)//2])
            
    else:
        value = int(input())
        bisect.insort_left(array, value)
        if len(array)%2 == 0:
            print(array[len(array)//2-1])
        else:
            print(array[len(array)//2])
            
        
    