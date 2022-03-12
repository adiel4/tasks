import sys,time
import sevseg
print('Countdown time is:')

secondsLeft=int(input('> '))
print('What message should we get in the end?')
MESSAGE=str(input('> '))

try:
    while True:
        print('\n' * 60)
        hours=str(secondsLeft//3600)
        minutes=str((secondsLeft%3600)//60)
        seconds=str(secondsLeft%60)
        hDigits=sevseg.getSevSegStr(hours,2)
        hTopRow,hMidRow,hBotRow=hDigits.splitlines()
        mDigits=sevseg.getSevSegStr(minutes,2)
        mTopRow,mMidRow,mBotRow=mDigits.splitlines()
        sDigits=sevseg.getSevSegStr(seconds,2)
        sTopRow,sMidRow,sBotRow=sDigits.splitlines()
        print(hTopRow+'   '+mTopRow+'   '+sTopRow)
        print(hMidRow+' * '+mMidRow+' * '+sMidRow)
        print(hBotRow+' * '+mBotRow+' * '+sBotRow)
        if secondsLeft==0:
            print()
            print(str.upper('***  '+MESSAGE+'  ***'))
            break
        print()
        print('Press Ctrl-C to quit')
        
        time.sleep(1)
        secondsLeft-=1
except KeyboardInterrupt:
    print('CountDown')
    sys.exit()
                        