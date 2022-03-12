class LightSwitch():
    def __init__(self):
        self.switchIsOn=False

    def turnOn(self):
        self.switchIsOn=True

    def turnOff(self):
        self.switchIsOn=False

lS=LightSwitch()
print(lS.turnOn())
