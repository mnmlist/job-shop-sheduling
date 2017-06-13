from functools import partial
import random
import jobshop
import pso
import de
import ga


if __name__ == '__main__':

    filePath = 'instances/3'
    jobs = jobshop.readJobs(filePath)
    m = len(jobs[0])
    j = len(jobs)
    print("Chosen file:", filePath)
    print("Chosen algorithm:", 'GS')
    print("Number of machines:", m)
    print("Number of jobs:", j)
    jobshop.printJobs(jobs)
    random.seed(1)
    
    
    # GENETIC ALGORITHM
    select = ga.select_best
    recombine = ga.recombine_simpleCrossover
    mutate = partial(ga.mutate_permuteSubsequence, max_shuffle_fraction=8)
    cost, solution = ga.engine(jobs, select=select, recombine=recombine, mutate=mutate, maxTime=20)
    jobshop.printSchedule(jobs, solution)
    print('==============GENETIC ALGORITHM=================')
    jobshop.prettyPrintSchedule(jobs, solution)
    print('===============================')


    # DIFFERENTIAL EVOLUTION
    cost, solution = de.engine(jobs)
    jobshop.printSchedule(jobs, solution)
    print('===============DIFFERENTIAL EVOLUTION================')
    jobshop.prettyPrintSchedule(jobs, solution)
    print('===============================')

    # PSO
    mask = jobshop.makeMask(jobs)
    pso = pso.ParticleSwarmOptimizer(j * m, mask, jobs)
    solution = pso.optimize()
    jobshop.printSchedule(jobs, solution.posRep)
    print('===============PSO================')
    jobshop.prettyPrintSchedule(jobs, solution.posRep)
    print('===============================')


    # a solution for vorlesungsbeispiel
    prettyPrintSchedule(jobs, [0, 0, 1, 2, 1, 1, 2, 2, 0])
