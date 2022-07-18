abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
num = [1, 2, 3, 4, 5, 6, 7, 8]
num = num[::-1]
pos = input()
for i in range(8):
    for j in range(8):
        if abc.index(pos[0]) == j and num.index(int(pos[1])) == i:
            print('Q', end=' ')
        elif num.index(int(pos[1])) == i:
            print('*', end=' ')
        elif abc.index(pos[0]) == j:
            print('*', end=' ')
        elif abs(num.index(int(pos[1]))-i)==abs(abc.index(pos[0])-j):
            print('*', end=' ')
        else:
            print('.', end=' ')
    print()
