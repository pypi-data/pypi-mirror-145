import cmath
def addOne(number):
    return number + 1
def addDouble(number):
    return number * 2
def add(distance,number):
    return number + distance
def stepUpTimes(times,number):
    return number + times * number
def numberTimes(times,number):
    return number * times
def aNumberOfFactorial(number):
    result = 1
    for item in range(1,number+1):
        result = result * item
    return result
def squareRoot_negativeNumber(number):
    num_sqrt = cmath.sqrt(number)
    copiseded_numbertimes = '{0} 的平方根为 {1:0.3f}+{2:0.3f}j'.format(number,
    num_sqrt.real,num_sqrt.imag)
    return copiseded_numbertimes

def squareRoot_positiveNumber(number):
    num_sqrt = number ** 0.5
    copiseded_number = ' %0.3f 的平方根为 %0.3f'%(number ,num_sqrt)
    return copiseded_number
def squareOfANumber(number):
    result = number * number
    return result
def division(Divisor,Dividend):
    result = 'the quotient is: %s'% (Dividend/Divisor)
    return result
