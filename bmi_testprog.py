import random
from os import path
from operator import add
from operator import sub
from operator import mul
from operator import mod
from operator import neg
from operator import lshift
from operator import rshift
from operator import abs
from operator import lt
from operator import le
from operator import eq
from operator import ne
from operator import ge
from operator import gt
from operator import xor
from operator import and_
from operator import or_
from operator import not_

import pandas

if __name__ == '__main__':
    filename = path.join('data', 'bmi_test.csv')

    data = pandas.read_csv(filename, sep=';')

    def protectedDiv(left, right):
        try: return left / right
        except ZeroDivisionError: return 1

    def func(kg, m):
        # return protectedDiv(kg, mul(m, m))
        #return abs(protectedDiv(mul(protectedDiv(kg, m), add(m, kg)), neg(neg(mul(add(m, kg), m))))) # Scores: (2.429324850286968, 1000.0)
        #return protectedDiv(abs(kg), mul(m, m)) # Scores: (2.429324850287263, 1000.0)
        return abs(protectedDiv(kg, mul(m, m))) # Scores: (2.429324850287263, 1000.0)

    correct = 0
    total = 0
    for item in data.itertuples():
        total = total + 1
        result = func(item.kg, item.m)
        diff = abs(item.bmi - result)
        is_correct = 'Correct' if diff < 0.5 else ''
        if is_correct:
            correct = correct + 1
        #print(item.kg, item.m, '=', item.bmi, 'vs', result, diff, is_correct)

    print('Correct:', correct, '/', total)
