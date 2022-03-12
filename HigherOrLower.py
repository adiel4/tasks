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
print('')