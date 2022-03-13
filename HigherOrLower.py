import random

suit_tuple=('Spades','Hearts','Clubs','Diamonds')
rank_tuple=('Ace','2','3','4','5','6','7','8','9')

nCards=8

def getCard(deckListIn):
    thisCard=deckListIn.pop()
    return thisCard

def shuffle(deckListIn):
    deckListOut=deckListIn.copy()
    random.shuffle(deckListOut)
    return deckListOut

print('Welcome to the game!!')
print('You have 50 points')
print()

startingDeckList=[]
for suit in suit_tuple:
    for thisValue,rank in enumerate(rank_tuple):
        cardDict={'rank':rank,'suit':suit,
        'value':thisValue+1}
        startingDeckList.append(cardDict)
score=50
while True:
    print()
    gameDeckList=shuffle(startingDeckList)
    currentCardDict=getCard(gameDeckList)
    currentCardRank=currentCardDict['rank']
    currentCardValue=currentCardDict['value']
    currentCardSuit=currentCardDict['suit']
    print('starting card is: ',currentCardRank+' of '+currentCardSuit)
    print()


    for cardNumber in range(0,nCards):
        answer=input('Will the next card be higher of lower than the '+
        currentCardRank+' of '+
        currentCardSuit+'? (enter h or l):')
        answer=answer.casefold()
        nextCardDict=getCard(gameDeckList)
        nextCardRank=nextCardDict['rank']
        nextCardSuit=nextCardDict['suit']
        nextCardValue=nextCardDict['value']
        print('Next card is:', nextCardRank+' of '+nextCardSuit)
        if answer=='h':
            if nextCardValue>currentCardValue:
                print('You are right, its h')
                score=score+20
            else:
                print('Wrong')
                score=score-15

        elif answer=='l':
            if nextCardValue<currentCardValue:
                score=score+20
                print('You are right, its l')
            else:
                score=score-15
                print('Wrong')
        print('Your score is:',score)
        print()
        currentCardRank=nextCardRank
        currentCardValue=nextCardValue
    goAgain=input('ENTER or q to play again:')
    if goAgain=='q':
        break
print('OK bye')
