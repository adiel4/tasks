def turnOn():
    global switchIsOn
    switchIsOn=False

def turnOff():
    global switchIsOn
    switchIsOn=True

switchIsOn=False
turnOn()
print(switchIsOn)
turnOff()
print(switchIsOn)
turnOn()
print(switchIsOn)
turnOff()
print(switchIsOn)
