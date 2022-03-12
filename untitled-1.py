#for x in range(10):
    #if x <= 3:
        #print(x, 'is less than or equal to three')
    #elif x > 5:
        #print(x, 'is greater than five')
    #else:
        #print(x, 'must be four or five , then')
        
#for x in range(10):
    #if x % 2:
        #print(x, 'is odd!')
    #else:
        #print(x, 'is even!')     
#year=1900        
#if not year % 400:
    #is_leap_year = True
#elif not year % 100:
    #is_leap_year = False
#elif not year % 4:
    #is_leap_year = True
#else:
    #is_leap_year = False
    
##s_ly = 'is a' if is_leap_year else 'is not a'
##print('{:4d} {:s} leap year'.format(year , s_ly))

#a,b=1071,462
#while b:
    #a,b=b,a%b
##print(a)

#x = 0
#while True:
    #x += 1
    #if not (x % 15 or x % 25):
        #break
#print(x, 'is divisible by both 15 and 25')

#for i in range(1,11):
    #if i%2:
        #continue
    #print(i,'is even!')
    
#alist=[1,2,3,4,5,6,7]
#for i,a in enumerate(alist):
    #if a<0:
        #print(a,'occurs at index',i)
        #break
#else:
    #print('no neg num in list')

a=1013
b=a-1
while b!=1:
    if not a%b:
        print('the largest factor of ',a,'is',b)
        break
    b-=1
else:
    print(a,'is prime')
