from functools import partial
import optparse
import random
import jobshop
import pso
import de
import ga


if __name__ == '__main__':

    filePath = 'instances/vorlesungsbeispiel'
    jobs = readJobs(filePath)
    m = len(jobs[0])
    j = len(jobs)
    print("Chosen file:", filePath)
    print("Chosen algorithm:", 'GS')
    print("Number of machines:", m)
    print("Number of jobs:", j)
    printJobs(jobs)
    random.seed(1)
    
    
    # GENETIC ALGORITHM
    # select = geneticSearch.select_best
    # recombine = geneticSearch.recombine_simpleCrossover
    # mutate = partial(geneticSearch.mutate_permuteSubsequence, max_shuffle_fraction=8)
    # cost, solution = geneticSearchTemplate(jobs, select=select, recombine=recombine, mutate=mutate, maxTime=20)
    
    
    # DIFFERENTIAL EVOLUTION
    # cost, solution = differentialEvolution.engine(jobs)
    
    # PSO
    

    printSchedule(jobs, solution)
    print('===============================')
    prettyPrintSchedule(jobs, solution)
    print('===============================')
    # a solution for vorlesungsbeispiel
    # prettyPrintSchedule(jobs, [0, 0, 1, 2, 1, 1, 2, 2, 0])
