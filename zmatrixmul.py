A =[[1,2,3], 
    [4,5,6],
    [4,5,6]]

B =[[1,2,3], 
    [4,5,6], 
    [4,5,6]]

result = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
newlist = [[]]

for i in range(len(A)):
    for j in range(len(B)):
        for k in range(len(B)):
            result[i][j] += A[i][k] * B[k][j]


print(result)


import numpy as np

ans=np.multiply(A,B)
print(ans)

