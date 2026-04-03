# t,w = map(int,input().split())
# data = [0] + [int(input()) for _ in range(t)]
# dp = [[0 for _ in range(w+1)] for _ in range(t+1)]
# for i in range(1,t+1):
#     if data[i]==1:
#         dp[i][0] = dp[i-1][0]+1
#     else:dp[i][0] = dp[i-1][0]
    
#     for j in range(1,w+1):
#         if (data[i]==1 and j%2==0) or (data[i]==2 and j%2!=0):
#             dp[i][j] = max(dp[i-1][j], dp[i-1][j-1])+1
#         else:
#             dp[i][j] = max(dp[i-1][j], dp[i-1][j-1])
# print(max(dp[t]))



# def parametric_search(arr):
#     cur = -1 
#     step = len(arr)
    
#     while step != 0: 
#         while (cur + step <len(arr) ) and arr[cur+step] ==False: 
#             cur+=step 
#         step//=2
#     return cur 
            



arr = [True,True,True,True,True,True,True,True,True,True,True,False,False,False,False]
arrs = [False, False, False,False,True,True,True,True,True,True,True,True,True,True,True]  


# print(parametric_search(arr))
# print(parametric_search(arrs))


# def parametric_search(arr): 
    
#     cur = -1
#     step = len(arr)
    
#     while step !=0:
        
#         while cur + step <len(arr) and  arr[cur+step] == True:
#             cur+=step
#         step//=2
    
#     return cur 



def parametric_search(arr):
    
    cur = -1
    step = len(arr)
    
    while step != 0:
        while cur+step<len(arr) and arr[cur+step]==True:
            cur+=step 
        step//=2 
    
    return cur 
            
print(parametric_search(arr))
print(parametric_search(arrs))
