from random import uniform

print('kg;m;bmi')

n = 10000

for _ in range(n):
    kg = round(uniform(20, 200), 1)
    m = round(uniform(0.6, 2), 2)
    bmi = round(kg / (m * m), 2)

    print('%s;%s;%s' % (kg, m, bmi))
