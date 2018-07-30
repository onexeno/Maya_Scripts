def padZero(number,zeroCount):
    temp = ''
    i = 0
    while i< zeroCount - len(str(number)):
        temp += '0'
        i+=1    
    #for i in range(0,zeroCount - len(str(number))):
    #   temp += '0'
    return temp+str(number)


