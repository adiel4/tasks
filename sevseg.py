
def getSevSegStr(number,minWidth=0):
    """Возвращает строковое значение для цифры на семисегментном
    индикаторе. Если возвращаемое строковое значение меньше minWidth,
    оно дополняется нулями."""
    number=str(number).zfill(minWidth)
    rows=['','','']
    for i,numeral in enumerate(number):
        if numeral=='.':
            rows[0]+=' '
            rows[1]+=' '
            rows[2]+='.'
            continue
        elif numeral=='-':
            rows[0]+=' '
            rows[1]+='--'
            rows[2]+=' '
        elif numeral=='0':
            rows[0]+=' __ '
            rows[1]+='|  |'
            rows[2]+='|__|'
        elif numeral=='1':
            rows[0]+='   '
            rows[1]+='  |'
            rows[2]+='  |'
        elif numeral=='2':
            rows[0]+=' __ '
            rows[1]+=' __|'
            rows[2]+='|__ '
        elif numeral=='3':
            rows[0]+=' __ '
            rows[1]+=' __|'
            rows[2]+=' __|'
        elif numeral=='4':
            rows[0]+='    '
            rows[1]+='|__|'
            rows[2]+='   |'
        elif numeral=='5':
            rows[0]+=' __ '
            rows[1]+='|__ '
            rows[2]+=' __|'            
        elif numeral=='6':
            rows[0]+=' __ '
            rows[1]+='|__ '
            rows[2]+='|__|'
        elif numeral=='7':
            rows[0]+=' __ '
            rows[1]+='   |'
            rows[2]+='   |'
        elif numeral=='8':
            rows[0]+=' __ '
            rows[1]+='|__|'
            rows[2]+='|__|'
        elif numeral=='9':
            rows[0]+=' __ '
            rows[1]+='|__|'
            rows[2]+=' __|'
        if i!= len(number)-1:
            rows[0]+=' '
            rows[1]+=' '
            rows[2]+=' '
    return '\n'.join(rows)

if __name__=='__main__':
    print()