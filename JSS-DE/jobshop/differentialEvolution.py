from .jobshop import *
import random
import time
import operator

def select_best(jobs, population, fraction=0.5):
    """Keep best fraction (in [0, 1]) of population"""
    population.sort()
    # get an even number of individuals
    # return population[:(populationSize//4) * 2]
    # select best half
    return population[:max(int(fraction * len(population)), 1)]


def select_richard(jobs, population, dividend=5):
    # richard selection: partition population and keep best of fraction of group
    nextGen = []
    counter = 0
    while counter < len(population):
        nextOffset = random.randint(2, int(len(population) / dividend))
        subPopulation = population[counter:counter + nextOffset]
        nextGen.extend(select_best(jobs, subPopulation))
        counter += nextOffset
    return nextGen


def select_stochastic(jobs, population):
    # stochastic selection
    # better solutions have greater chance to stay but may also be killed
    population = sorted(population)
    nextGen = []
    populationSize = len(population)
    while nextGen == []:
        for i in range(populationSize):
            randomNumber = random.randint(0, populationSize)
            if i < randomNumber:
                nextGen.append(population[i])
            else:
                pass
    return nextGen


def recombine_simpleCrossover(jobs, s1, s2):
    # Recombine with classic crossover
    cut = random.randint(0, len(s1) - 1)
    return normalizeSchedule(jobs, s1[:cut] + s2[cut:])


def mutate_permuteSubsequence(jobs, s, max_shuffle_fraction=4):
    """Mutate by random.shuffling a subsequence of a schedule."""
    a, b = sorted([random.randint(0, len(s) - 1), random.randint(0, len(s) - 1)])

    # The mutation should not be too large.
    # TODO maybe just:
    # b = random.randint(a, j*m//constant)
    # TODO think about probabilities...
    b = min(b, a + len(s) // max_shuffle_fraction)

    shuffle(s, a, b)


def mutate_swap(jobs, s, num_swaps=5):
    """Mutate by swapping two instructions."""
    for swap in range(num_swaps):
        a = random.randint(0, len(s) - 1)
        b = random.randint(0, len(s) - 1)
        s[a], s[b] = s[b], s[a]


def engine(jobs, populationSize=100, maxTime=None):
    """
    Differential Evolution algorithm for the jobshop scheduling problem.
    """

    numGenerations = 10  # generations calculated between logging
    solutions = []  # list of (time, schedule) with decreasing time
    best = 10000000  # TODO set initial value for max of add check in loop

    j = len(jobs)
    m = len(jobs[0])
    l = j * m
    CR = 0.7
    F = random.random() * 2
    genLength = j * m

    # initial generation
    schedules = [randomSchedule(j, m) for i in range(populationSize)]
    fitness = [cost(jobs, s) for s in schedules]
    population = list(zip(fitness, schedules))

    for idx in range(numGenerations):
        for iPopulation in range(populationSize):
            # calculate new candidate solution
            y = population[iPopulation]
            # pick 3 different random points from population
            while True:
                agentIdxA, agentIdxB, agentIdxC = random.sample(range(0, numGenerations), 3)
                if ((agentIdxA != idx) and (agentIdxB != idx) and (agentIdxC != idx)):
                    break
            # pick a random index [0-Dimensionality]
            R = random.randint(0, len(population[0][1]))

            # compute the agent's new position
            for genIdx in range(genLength):
                r = random.random()
                if (r < CR) or (genIdx == R):
                    normalizedSchedule = randomSchedule(j, m)

            normalizedCost = cost(jobs, normalizedSchedule)
            if (normalizedCost < population[iPopulation][0]):
                population[iPopulation] = (normalizedCost, normalizedSchedule)

        costArray = [e[0] for e in population]
        minI, minV = min(enumerate(costArray), key=operator.itemgetter(1))
        best_individuum = population[minI]

        if best_individuum[0] < best:
            best = best_individuum[0]
            solutions.append(best_individuum)

    solutionGen = normalizeSchedule(jobs, solutions[0][1])
    solutionCost = solutions[0][0]
    return (solutionCost, solutionGen)
