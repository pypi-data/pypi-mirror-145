import random
def randomInt_Float(fromInt,toInt):
    randomnum = random.uniform(fromInt,toInt)
    return randomnum
def randomInt_Integers(fromInt,toInt):
    randomnumber = random.randint(fromInt,toInt)
    return randomnumber
def randomInt_type_MaxMinNumber():
    #使用循环取值支持输入，并检测异常，冒泡输入8位
    list_1 = list()
    try:
        for i in range(8):
            num = eval(input('请输入数字'))
            list_1.append(num)
        print(list_1)
        c = list_1[0]
        list_max = max(list_1)
        list_min = min(list_1)
        print('max:',list_max)
        print('min:',list_min)
    except Exception as e:
        print(e)
    return
