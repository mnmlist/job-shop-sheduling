from jobshop import *
from jobshop import differentialEvolution

from functools import partial
import optparse
import random

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
    cost, solution = differentialEvolution.engine(jobs)

    printSchedule(jobs, solution)
    print('===============================')
    prettyPrintSchedule(jobs, solution)
    print('===============================')
    # a solution for vorlesungsbeispiel
    # prettyPrintSchedule(jobs, [0, 0, 1, 2, 1, 1, 2, 2, 0])
