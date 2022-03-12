from datetime import datetime
class Customer:
    """ Класс, представляющий клиента банка. """
    def __init__(self,name,address,date_of_birth):
        self.name=name
        self.address=address
        self.date_of_birth=datetime.strptime(date_of_birth,'%Y-%m-%d')
        self.password='1234'
    
    def get_age(self):
        """ Вычисляет и возвращает возраст клиента. """
        today=datetime.today()
        try:
            birthday=self.date_of_birth.replace(year=today.year)
        except ValueError:
            birthday=self.date_of_birth.replace(year=today.year,day=self.date_of_birth.day-1)
        if birthday>today:
            return today.year-self.date_of_birth.year-1
        return today.year-self.date_of_birth.year