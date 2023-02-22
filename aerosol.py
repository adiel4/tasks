# class Solution:
#     def addToArrayForm(self, num: List[int], k: int) -> List[int]:
#         a= num
#         b= "".join([str(i) for i in a])
#         print(b)
#         k = 25
#         return [int(j) for j in str(int(b)+ k)]

# nums = [3,2,4]
# target = 6

# for i in range(len(nums)):
#     for k in range(1, len(nums)):
#         if i+k ==target:
#             print(nums[i],nums[k])
#             break
#         break
import numpy as np
print(np.ceil(-1.9798))