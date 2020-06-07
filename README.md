# Genetic programming experiment: BMI calculator

## General info

I experimented with genetic programming part of [DEAP](https://github.com/DEAP/deap) library to figure out the tricky parts of process. Goal was to train and generate function to calculate body mass index from example data. Learned: available function selection and validation/fitenss checker has huge impact on how quickly the algorithm finds correct and compact solution for even simple function like BMI.

## Usage

Install dependencies and generate test/training datasets as CSV. Training was done with only 1000 rows and testing was done with 10000 lines.

```
$ pipenv install
$ pipenv run python bmi_generate.py > data/bmi_train.csv
$ pipenv run python bmi_generate.py > data/bmi_test.csv
```

Run genetic program synthesis and optimization. This might take a while.

```
$ pipenv run python bmi_geneticprog.py

                                              fitness                                                         size
                -------------------------------------------------------------------     -----------------------------------------------
gen     nevals  avg             gen     max             min     nevals  std             avg     gen     max     min     nevals  std
0       300     1.89877e+12     0       1.13926e+15     0       300     4.64714e+13     5.81333 0       15      2       300     3.39782
1       166     72821           1       1.42771e+07     0       166     706574          6.07    1       18      2       166     3.45713
2       139     16833           2       200504          0       139     33536.1         8.69333 2       20      2       139     3.93183
3       158     16216.2         3       307128          0       158     38454           9.08333 3       20      3       158     3.16908

...

998     187     13259.7         998     89089.9         0       187     28965.4         4.82667 998     7       3       187     1.00497
999     165     11124.9         999     89089.9         0       165     26018.4         4.82667 999     7       3       165     1.01815
1000    167     9487.34         1000    89089.9         0       167     23384.9         4.78    1000    7       3       167     1.00246
Program: protectedDiv(kg, mul(m, m)) Scores: (2.429324850287263, 1000.0)
Program: add(protectedDiv(add(m, kg), mul(m, m)), abs(protectedDiv(m, kg))) Scores: (869.5251596487444, 0.0)
Program: add(protectedDiv(add(m, kg), mul(m, m)), abs(protectedDiv(m, protectedDiv(add(m, kg), mul(m, m))))) Scores: (888.6131776319143, 0.0)
Program: add(protectedDiv(add(mod(m, m), kg), mul(m, m)), abs(protectedDiv(m, m))) Scores: (1000.0037479362775, 0.0)
Program: add(protectedDiv(add(m, kg), mul(m, abs(m))), abs(protectedDiv(m, m))) Scores: (1852.6384506432505, 0.0)
```

Solutions programs can be tested by copying the program code from solution list into body of `func()` in `bmi_testprog.py` and running it.

```
$ pipenv run python bmi_geneticprog.py
Correct: 10000 / 10000
```

## TODO

 * Figure out why DEAP multiprocessing is not working, speeds up training
 * Test with DEAP typed primitives/functions
 * Research and test better fitness functions
