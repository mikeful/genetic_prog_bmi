import operator
import random
from os import path

import numpy
import pandas

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

if __name__ == '__main__':
    filename = path.join('data', 'bmi_train.csv')

    data = pandas.read_csv(filename, sep=';')

    def evalChecksum(individual, data):
        func = toolbox.compile(expr=individual)

        score = 0
        correct = 0
        for item in data.itertuples():
            # Run generated function, on errors return high penalty score
            try:
                result = func(item.kg, item.m)
            except ZeroDivisionError:
                return (9999, 0)
            except OverflowError:
                return (9999, 0)
            except MemoryError:
                return (9999, 0)
            except ValueError:
                return (9999, 0)
            except TypeError:
                return (9999, 0)

            # Reward for correct calculation
            # = smaller difference between result and expected result
            diff = abs(item.bmi - result)
            score = score + diff

            if diff < 0.5:
                correct = correct + 1

        return (score, correct)

    def protectedDiv(left, right):
        try: return left / right
        except ZeroDivisionError: return 1

    # Setup prgram tree and parameters
    pset = gp.PrimitiveSet("MAIN", 2)
    pset.renameArguments(ARG0='kg')
    pset.renameArguments(ARG1='m')

    # Setup available variables and functions
    # pset.addEphemeralConstant("rand100", lambda: random.randint(-100, 100))
    # pset.addEphemeralConstant("rand1", lambda: random.randint(-1, 1))
    # pset.addEphemeralConstant("rand10", lambda: random.randint(0, 10))
    pset.addPrimitive(protectedDiv, 2)
    pset.addPrimitive(operator.add, 2)
    pset.addPrimitive(operator.sub, 2)
    pset.addPrimitive(operator.mul, 2)
    pset.addPrimitive(operator.mod, 2)
    pset.addPrimitive(operator.neg, 1)
    pset.addPrimitive(operator.abs, 1)
    # pset.addPrimitive(operator.lt, 2)
    # pset.addPrimitive(operator.le, 2)
    # pset.addPrimitive(operator.eq, 2)
    # pset.addPrimitive(operator.ne, 2)
    # pset.addPrimitive(operator.ge, 2)
    # pset.addPrimitive(operator.gt, 2)
    # pset.addPrimitive(operator.lshift, 2)
    # pset.addPrimitive(operator.rshift, 2)
    # pset.addPrimitive(operator.xor, 2)
    # pset.addPrimitive(operator.and_, 2)
    # pset.addPrimitive(operator.or_, 2)
    # pset.addPrimitive(operator.not_, 1)

    # Setup algoritm and stats
    creator.create("FitnessMin", base.Fitness, weights=(-1.0, 1.0))
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=3)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("compile", gp.compile, pset=pset)

    toolbox.register("evaluate", evalChecksum, data=data)
    toolbox.register("select", tools.selTournament, tournsize=10)
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
    #toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
    toolbox.register("mutate", gp.mutShrink)

    # https://deap.readthedocs.io/en/master/api/tools.html#deap.gp.staticLimit"
    toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
    toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)

    # Run algoritm
    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(5)
    pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 1000, stats=mstats, halloffame=hof, verbose=True)

    #print(log)

    # Display solutions as function code and score
    for solution in hof:
        tree = gp.PrimitiveTree(solution)
        print('Program:', str(tree), 'Scores:', solution.fitness)
