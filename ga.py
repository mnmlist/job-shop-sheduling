import jobshop
import random
import time

def select_best(jobs, population, fraction=0.5):
    # Keep best fraction (in [0, 1]) of population
    population.sort()
    # get an even number of individuals
    # return population[:(populationSize//4) * 2]
    # select best half
    return population[:max(int(fraction * len(population)), 1)]


def recombine_simpleCrossover(jobs, s1, s2):
    """
     Recombine with classic crossover
    """
    cut = random.randint(0, len(s1) - 1)
    return jobshop.normalizeSchedule(jobs, s1[:cut] + s2[cut:])

def mutate_permuteSubsequence(jobs, s, max_shuffle_fraction=4):
    """
    Mutate by random.shuffling a subsequence of a schedule.
    """
    a, b = sorted([random.randint(0, len(s) - 1), random.randint(0, len(s) - 1)])

    # The mutation should not be too large.
    # TODO maybe just:
    # b = random.randint(a, j*m//constant)
    # TODO think about probabilities...
    b = min(b, a + len(s) // max_shuffle_fraction)

    jobshop.shuffle(s, a, b)



def engine(jobs, recombine, mutate=mutate_permuteSubsequence, select=select_best,
        populationSize=100, maxTime=None):
    # Genetic algorithm for the jobshop scheduling problem.

    numGenerations = 10   # generations calculated between logging
    solutions = []   # list of (time, schedule) with decreasing time
    best = 10000000

    t0 = time.time()
    totalGenerations = 0

    j = len(jobs)
    m = len(jobs[0])
    l = j*m

    # initial generation
    schedules = [jobshop.randomSchedule(j, m) for i in range(populationSize)]
    fitness = [jobshop.cost(jobs, s) for s in schedules]

    population = list(zip(fitness, schedules))

    while True:
        try:
            start = time.time()

            for g in range(numGenerations):
                # (1) selection
                fittest = select(jobs, population)

                # (2) recombination
                next_generation = []
                while len(fittest) + len(next_generation) < populationSize:
                    next_generation.append(
                        recombine(jobs, random.choice(fittest)[1], random.choice(fittest)[1]))

                population = fittest + [(0, s) for s in next_generation]

                # (3) mutation
                for _, individual in population:
                    mutate(jobs, individual)

                # reevaluate population
                population = [(jobshop.cost(jobs, i), i) for _, i in population]

                best_individuum = min(population)

                if best_individuum[0] < best:
                    best = best_individuum[0]
                    solutions.append(best_individuum)

                totalGenerations += 1

            print("Generation", totalGenerations)

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
            print("Found in {:} generations in {:.1f}s".format(totalGenerations, time.time() - t0))

            return solutions[-1]
