

class BankAccount:
    """Абстрактный базовый класс, представляющий банковский счет."""
    currency='$'
    def __init__(self,customer,account_number,balance=0):
        """
        Инициализация класса BankAccount значениями имени клиента, номера счета и
        баланса при открытии счета (по умолчанию 0).
        """
        self.customer=customer
        self.account_number=account_number
        self.balance=balance
    
    def deposit(self,amount):
        """Размер вклада на банковский счет."""
        if amount>0:
            self.balance+=amount
        else:
            print('INVALID DEPOSIT AMOUNT:',amount)
    
    def withdraw(self,amount):
        """
        Сумма средств, снимаемых с банковского счета, при условии достаточной суммы
        на этом счете.
        """   
        if amount>0:
            if amount>self.balance:
                print('Insufficient funds')
            else:
                self.balance-=amount
        else:
            print("INVALID WITHDRAWAL AMOUNT:", amount)
        
    def check_balance(self):
        """вывод состояния счета"""
        print('The balance of account number {:d} is {:s}{:.2f}'
              .format(self.account_number,self.currency,self.balance))
        
        
class SavingsAccount():
    """Класс, представляющий накопительный счет."""
    def __init__(self,customer,account_number,interest_rate,balance=0):
        """ Инициализация накопительного счета. """
        self.interest_rate=interest_rate
        super().__init__(customer,account_number,balance)
    def add_interest(self):
        """ Добавление процентной ставки к сумме счета с коэффициентом self.interest_rate. """
        self.balance*=(1+self.interest_rate/100)
        