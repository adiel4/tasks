import random

NUM_DIGITS=3 #количетсво цифр
MAX_GUESSES=10 #кол-во попыток

def main():
    print('''Bagels, a deductive logic game.
I am thinking of a {}-digit number with no repeated digits.
Try to guess what it is. Here are some clues:
When I say:   That means:
Pico          One digit is correct but in the wrong position.
Fermi         One digit is correct and in the right position.
Bagels        No digit is correct.
For example, if the secret number was 248 and your guess was 843, the
clues would be Fermi Pico.'''.format(NUM_DIGITS))
    while True: #основной цикл
        secretNum=getSecretNum()
        print('I have thought up a number')
        print('You have {} guesses to get it.'.format(MAX_GUESSES))
        
        numGuesses=1
        
        while numGuesses<=MAX_GUESSES:
            guess=''
            while len(guess)!=NUM_DIGITS or not guess.isdecimal():
                print('Guess #{}: '.format(numGuesses))
                guess=input('> ')
            clues=getClues(guess,secretNum)
            print(clues)
            numGuesses+=1
            if guess==secretNum:
                break
            if numGuesses> MAX_GUESSES:
                print('You ran out of guesses.')
                print('The answer was {}.'.format(secretNum))
        print('Do you want to play again? (yes or no)')
        if not input('> ').lower().startswith('y'):
            break
    print('Thanks for playing!')
    
def getSecretNum():
    """Возвращает строку из NUM_DIGITS уникальных случайных цифр."""
    numbers=list('0123456789')
    random.shuffle(numbers)
    secretNum=''
    for i in range(NUM_DIGITS):
        secretNum+=str(numbers[i])
    return secretNum

def getClues(guess,secretNum):
    """Возвращает строку с подсказками pico, fermi и bagels
    для полученной на входе пары из догадки и секретного числа."""
    if guess==secretNum:
        return 'You got it'
    clues=[]
    
    for i in range(len(guess)):
        if guess[i]==secretNum[i]:
            # Правильная цифра на правильном месте.
            clues.append('Fermi')
        elif guess[i] in secretNum:
            # Правильная цифра на неправильном месте.
            clues.append('Pico')
    if len(clues)==0:
        return 'Bagels' # Правильных цифр нет вообще.
    else:
        # Сортируем подсказки в алфавитном порядке, чтобы их исходный
        # порядок ничего не выдавал.        
        clues.sort()
        return' '.join(clues)


if __name__=='__main__':
    main()
            