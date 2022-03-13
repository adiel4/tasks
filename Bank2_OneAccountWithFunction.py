accountName=''
accountBalance=0
accountPassword=''

def NewAccount(name,balance,password):
    global accountName,accountBalance,accountPassword
    accountName=name
    accountBalance=balance
    accountPassword=password

def show(password):
    global accountName,accountBalance,accountPassword
    if password!=accountPassword:
        print('Incorrect password')
        return None
    return accountBalance

def getBalance(password):
    global accountName,accountBalance,accountPassword
    if password!=accountPassword:
        print('Incorrect password')
        return None
    return accountBalance

def deposit(amountToDeposit,password):
    global accountName,accountBalance,accountPassword
    if amountToDeposit<0:
        print('You cannot deposit a negative amount!')
        return None
    accountBalance=accountBalance+amountToDeposit
    return accountBalance

def withdraw(amountToWithdraw,password):
    global accountName,accountBalance,accountPassword
    if amountToWithdraw<0:
        print('You cannot withdraw a negative amount')
        return None
    if password!=accountPassword:
        print('Wrong password')
        return None
    if amountToWithdraw>accountBalance:
        print('You cannot withdraw more than you have')
        return None

    accountBalance=accountBalance-amountToWithdraw
    return accountBalance


NewAccount('Adilet',100,'adilet321')


while True:
    print()
    print('Press b to get the balance')
    print('Press d to make a deposit')
    print('Press w to make a withdrawal')
    print('Press s to show the account')
    print('Press q to quit')
    print()
    action=input('What do you want to do? ')
    action=action.lower()
    action=action[0]
    print()

    if action=='b':
        print('Get Balance:')
        userPassword=input('Please enter the password: ')
        theBalance=getBalance(userPassword)
        if theBalance is not None:
            print('Your balance is:',theBalance)
    elif action=='d':
        print('Deposit:')
        userDepositAmount=input('Please enter amount to deposit: ')
        userDepositAmount=int(userDepositAmount)
        userPassword=input('Please enter the password: ')
        newBalance=deposit(userDepositAmount, userPassword)
        if newBalance is not None:
            print('Your new balance is:',newBalance)
    elif action=='q':
        break
    elif action=='w':
        print('Withdrawal')
        userWithdrawAmount=input('Please enter amount to withdraw: ')
        userWithdrawAmount=int(userWithdrawAmount)
        userPassword=input('Enter the password: ')
        newBalance=withdraw(userWithdrawAmount, userPassword)
        if newBalance is not None:
            print('Your new balance is: ',newBalance)
    elif action=='s':

        userPassword=input('Enter the password: ')
        print('Account Information:')
        print('         Name:',accountName)
        print('         Balance:',show(userPassword))
        print('         password:',accountPassword)
        print()
print('Done')
