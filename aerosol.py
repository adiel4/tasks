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

import matplotlib.pyplot as plt

a = [1,10,100,1000,10000,100000]
b = [1,2,3,4,5,6]

fig,ax = plt.subplots()
ax.plot(a,b)

ax.set_xlabel('adilet')

ax2 = ax.twiny()

# set the limits of the second x-axis to be the same as the first
ax2.set_xlim(ax.get_xlim())

# set the label of the second x-axis
ax2.set_xlabel('Additional X-axis Label')

# hide the tick marks and tick labels of the second x-axis
ax2.xaxis.set_ticks_position('none')
ax2.set_xticklabels()

# show the plot
plt.show()