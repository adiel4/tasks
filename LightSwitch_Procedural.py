def turnOn():
    global switchIsOn
    SwitchIsOn=True

def turnOff():
    global switchIsOn
    switchIsOn=False

switchIsOn=False
print(switchIsOn)
turnOn()
print(switchIsOn)
turnOff()
print(switchIsOn)

print(switchIsOn)
