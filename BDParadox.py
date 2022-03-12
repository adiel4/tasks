"""Имитационное моделирование парадокса дней рождения, (c) Эл Свейгарт
al@inventwithpython.com Изучаем неожиданные вероятности из "Парадокса
дней рождения". Больше информации — в статье
https://ru.wikipedia.org/wiki/Парадокс_дней_рождения
Код размещен на https://nostarch.com/big-book-small-python-projects
Теги: короткая, математическая, имитационное моделирование"""
import datetime, random

def getBirthday(numberOfBirthdays):
    """ Возвращаем список объектов дат для случайных дней рождения."""
    birthdays=[]
    for i in range(numberOfBirthdays):
        # Год в нашем имитационном моделировании роли не играет, лишь
        # бы в объектах дней рождения он был одинаков.
        startofYear=datetime.date(2001,1,1)
        randomNumberofDays=datetime.timedelta(random.randint(0,364))
        birthday=startofYear+randomNumberofDays
        birthdays.append(birthday)
    return birthdays


def getMatch(birthdays):
    """ Возвращаем объект даты дня рождения, встречающегося
    несколько раз в списке дней рождения."""
    
    if len(birthdays)==len(set(birthdays)):
        return None # Все дни рождения различны, возвращаем None.
    # Сравниваем все дни рождения друг с другом попарно:
    for a,birthadayA in enumerate(birthdays):
        for b,birthdayB in enumerate(birthdays[a+1:]):
            if birthadayA==birthdayB:
                return birthadayA   # Возвращаем найденные соответствия.
print('''Birthday Paradox, by Al Sweigart al@inventwithpython.com
The Birthday Paradox shows us that in a group of N people, the odds
that two of them have matching birthdays is surprisingly large.
This program does a Monte Carlo simulation (that is, repeated random
simulations) to explore this concept.
(It's not actually a paradox, it's just a surprising result.)
''')
# Создаем кортеж названий месяцев по порядку:
MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
while True: # Запрашиваем, пока пользователь не введет допустимое значение.
    print('How many birthdays shall I generate? (Max 100)')
    response = input('> ')
    if response.isdecimal() and (0 < int(response) <= 100):
        numBDays = int(response)    
        break # Пользователь ввел допустимое значение.
print()
# Генерируем и отображаем дни рождения:
print('Here are', numBDays, 'birthdays:')
birthdays = getBirthday(numBDays)
for i,birthday in enumerate(birthdays):
    if i!=0:
        print('\t',end='')
    monthName=MONTHS[birthday.month-1]
    dateText='{} {}'.format(monthName,birthday.day)
    print(dateText,end='')
    
print()
print()

match=getMatch(birthdays)

# Отображаем результаты:
print('In this simulation, ',end='')
if match!=None:
    monthName=MONTHS[match.month-1]
    dateText='{} {}'.format(monthName,match.day)
    print('multiple people have a birthday on ',dateText)
else:
    print('there are nomatching birthdays')
print()

print('Generating', numBDays, 'random birthdays 100,000 times...')
input('Press Enter to begin...')

print('Let\'s run another 100,000 simulations.')
simMatch = 0 # Число операций моделирования с совпадающими днями рождения.
for i in range(100_000):
    if i%10_000==0:
        print(i,'simulations run...')
    birthdays=getBirthday(numBDays)
    if getMatch(birthdays)!=None:
        simMatch=simMatch+1
print('100,000 simulations run.')

probability = round(simMatch / 100_000 * 100, 2)
print('Out of 100,000 simulations of', numBDays, 'people, there was a')
print('matching birthday in that group', simMatch, 'times. This means')
print('that', numBDays, 'people have a', probability, '% chance of')
print('having a matching birthday in their group.')
print('That\'s probably more than you would think!')