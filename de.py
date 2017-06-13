import jobshop
import random
import time
import operator


def engine(jobs, populationSize=100, maxTime=None):
    """
    Differential Evolution algorithm for the jobshop scheduling problem.
    """

    numGenerations = 10  # generations calculated between logging
    solutions = []  # list of (time, schedule) with decreasing time
    best = 10000000  # TODO set initial value for max of add check in loop
    t0 = time.time()
    j = len(jobs)
    m = len(jobs[0])
    l = j * m
    CR = 0.7
    F = random.random() * 2
    genLength = j * m

    # initial generation
    schedules = [jobshop.randomSchedule(j, m) for i in range(populationSize)]
    fitness = [jobshop.cost(jobs, s) for s in schedules]
    population = list(zip(fitness, schedules))

    while True:
        try:
            start = time.time()

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
                            normalizedSchedule = jobshop.randomSchedule(j, m)

                    # compute cost for normalized schedule
                    normalizedCost = jobshop.cost(jobs, normalizedSchedule)

                    # if new schedule better then update agent in population
                    if (normalizedCost < population[iPopulation][0]):
                        population[iPopulation] = (normalizedCost, normalizedSchedule)

                costArray = [e[0] for e in population]
                minI, minV = min(enumerate(costArray), key=operator.itemgetter(1))
                best_individuum = population[minI]

                # update best individuum
                if best_individuum[0] < best:
                    best = best_individuum[0]
                    solutions.append(best_individuum)

            if maxTime and time.time() - t0 >= maxTime:
                raise jobshop.OutOfTime("Time is over")

            t = time.time() - start
            if t > 0:
                print("Best:", best, "({:.1f} Generations/s, {:.1f} s)".format(
                        numGenerations, time.time() - t0))
                print('time: ',time.time() - t0)
            # Make outputs appear about every 3 seconds.
            if t > 4:
                numGenerations //= 2
            elif t < 1.5:
                numGenerations *= 2

        except (KeyboardInterrupt, jobshop.OutOfTime) as e:
            print()
            print("================================================================================")
            print("Best solution:")
            print(solutions[-1][1])

            return solutions[-1]


