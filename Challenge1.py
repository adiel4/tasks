import math
import numpy as np
#num1=input("Inpurt number 1:")
#num2=input("Inpurt number 2:")
#if num1>num2:
    #print(str(num2)+'\n'+str(num1))
#else:
    #print(str(num1)+'\n'+str(num2))
       
#num1=int(input('Input number less than 20:'))
#if num1>=20:
    #print('Too high!')
#else:
    #print('Thank you!')
    
#num=int(input('Enter number a number between 10 and 20(inclusive):'))
#if num>=10 and num<=20:
    #print('thank you!')
#else:
    #print('incorrect answer')
    
#color=input('What is your favourite colour? ')
#if color=='RED' or color=='red' or color=='Red':
    #print('I like red too!')
#else:
    #print('I dont like '+color+', I prefer red')
    
#ans1=input('Is it raining outside? ')
#ans1=str.lower(ans1)
#ans2=input('Is it windy outside? ')
#ans2=str.lower(ans2)
#if ans2=='yes':
    #print('It is too windy for an umbrella')
#elif ans1=='yes':
    #print('Take an umbrella')
#else:
    #print('Enjoy your day')
    
#age=int(input('Users age:'))
#if age>=18:
    #print('You can vote')
#elif age==17:
    #print('You can learn to drive')
#elif age==16:
    #print('You can buy a lottery ticket')
#else:
    #print('You can go Trick-or-Treating')
    
#num=int(input('enter a number:'))
#if num<10:
    #print('Too low')
#elif num>20:
    #print('Too high')
#else:
    #print('Correct')
    
#num=int(input('Enter 1 or 2 or 3:'))
#if num==1:
    #print('Thank you!')
#elif num==2:
    #print('Well done')
#elif num==3:
    #print('Correct')
#else:
    #print('Error message')
    
#name=input('Enter your name:')
#print(len(name))

#sur=input('Enter your surname:')
#fullName=name+' '+sur
#print(fullName,len(fullName)-1)

#fullName=str.title(fullName)
#print(fullName)

a=541
#print(round(math.sqrt(a),2))
num=5
def make_negative(num):
    return -num if num>0 else num
#print(make_negative(5),make_negative(-4))
def summation(num):
    sum=1
    while num>1:
        sum=sum+num
        num=num-1
    return sum
#print(summation(3))
def sumbest(num):
    return sum(range(num+1))
def sumbest2(num):
    return (1+num)*num/2
#print(sumbest2(5))
def longest(a1,a2):
    a=a1+a2
    return a
#print(longest("aretheyhere","yestheyarehere"))
def get_middle(a):
    if len(a)%2!=0:
        mid=a[round((len(a)-1)/2)]
    else:
        mid=a[round((len(a)-2)/2)]+a[round((len(a))/2)]
    return mid
def get_middlebetter(a):
   return a[round((len(a)-1)/2):round((len(a)-1)/2+1)]
#print(get_middlebetter('adiletibraev'))

def positive_sum(arr):
    return sum(x for x in arr if x > 0)

#print(positive_sum([1,2,3,4,5,-5,-5,15]))

def invert(arr):
    for i in range(0,len(arr)):
        arr[i]=-arr[i]
    return arr
def invert_better(arr):
    return [-x for x in arr]
#print(invert_better([1,2,-3,-7,5,-6]))
def is_isogram(word):
    word=str.lower(word)
    for i in word:
        print(i)
    pass
#print(is_isogram('adilat'))
def xob(s):
    s=s.lower()
    return s.count('x')==s.count('o')

def abbrevName(name):
    return '.'.join(w[0] for w in name.split()).upper()
#print(abbrevName('adil eib'))

def maps(a):
    for i in range(0,len(a)):
        a[i]=2*a[i]
    return a
def mapsb(a):
    return [2*x for x in a]
#print(mapsb([1,2,3,4]))
def square_sum(a):
    return sum([x**2 for x in a])
#print(square_sum([1,2,2]))
def find_it(seq):
    return [x for x in seq if seq.count(x)%2!=0][0]

#print(find_it([20,1,-1,2,-2,3,3,5,5,1,2,4,20,4,-1,-2,5]))

def high_and_low(numbers):
    return str(max([int(x) for x in numbers.split(' ')]))+' '+str(min([int(x) for x in numbers.split(' ')]))
    pass
#print(high_and_low("1 2 3 4 5"))
def validate_pin(d):
    return (len(d)==4 or len(d)==6) and len([True for x in list(d) if x.isdigit()==True])==len(d)

#print(validate_pin('12437'))

def validate_pin_better(pin):
    return len(pin) in (4, 6) and pin.isdigit()

#print(validate_pin_better('1234'))


def disemvowel(string_):
    return ''.join([string_[i] for i in range(0,len(string_)) if string_[i]!='a' and string_[i]!='i' and string_[i]!='e' and string_[i]!='o' and string_[i]!='u'])
    pass
def disemvowel2(string_):
    return string_.replace('a','').replace('i','').replace('e','').replace('u','').replace('o','').replace('A','').replace('I','').replace('E','').replace('U','').replace('O','')
def disemvowelbetter(string):
    return "".join(c for c in string if c.lower() not in "aeiou")
#print(disemvowelbetter('adilet Ibraev'))

def bouncing_ball(h, bounce, window):
    i=1
    if h<=0:
        return -1
    elif bounce<=0 or bounce>=1:
        return -1
    elif window>=h:
        return -1
    else:
        while window<h:
            h=h*bounce
            i=i+1
        return i

def to_roman(val):
    rNum=['I','II','III','IV','V','VI','VII','VIII','IX','X','XL','L','LX','LXX','LXX','LXXX','XC','C','CD','D','DC','DCC','DCCC','CM','M']
    Num=[1,2,3,4,5,6,7,8,9,10,40,50,60,70,80,90,100,400,500,600,700,800,900,1000]
    rNum2=rNum[::-1]
    Num2=Num[::-1]
    
    return ''.join(romNum)

def from_roman(roman_num):
    rNum=['I','II','III','IV','V','VI','VII','VIII','IX','X','XL','L','LX','LXX','LXX','LXXX','XC','C','CD','D','DC','DCC','DCCC','CM','M']
    Num=[1,2,3,4,5,6,7,8,9,10,40,50,60,70,80,90,100,400,500,600,700,800,900,1000]
    rNum2=rNum[::-1]
    Num2=Num[::-1]
    return rNum2,Num2

import string
def is_pangram(s):
    alph=list('abcdefghijklmonpqrstuwxyz')
    for word in s.split(' '):
        for i in list(str.lower(word)):
            if i in alph:
                alph.pop(alph.index(i))
            else:
                continue
    if alph==[]:
        return True
    else:
        return False
def is_pangrambetter(s):
    s = s.lower()
    for char in 'abcdefghijklmnopqrstuvwxyz':
        if char not in s:
            return False
    return True
            
        
def friend(x):
    return [name for name in x if len(name)==4]
    pass


def tower_builder(n_floors):
    tower=['*'*(2*i-1) for i in range(1,n_floors+1)]
    
    return tower
    pass

print(tower_builder(3))