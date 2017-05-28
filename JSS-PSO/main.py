from jobshop import *
from jobshop import differentialEvolution

from functools import partial
import optparse
import random
#
# if __name__ == '__main__':
#
#     filePath = 'instances/vorlesungsbeispiel'
#     jobs = readJobs(filePath)
#     m = len(jobs[0])
#     j = len(jobs)
#     print("Chosen file:", filePath)
#     print("Chosen algorithm:", 'GS')
#     print("Number of machines:", m)
#     print("Number of jobs:", j)
#     printJobs(jobs)
#     random.seed(1)
#     cost, solution = differentialEvolution.engine(jobs)
#
#     printSchedule(jobs, solution)
#     print('===============================')
#     prettyPrintSchedule(jobs, solution)
#     print('===============================')
#     # a solution for vorlesungsbeispiel
#     # prettyPrintSchedule(jobs, [0, 0, 1, 2, 1, 1, 2, 2, 0])

import random

w = 0.729844  # Inertia weight to prevent velocities becoming too large
c1 = 1.496180  # Scaling co-efficient on the social component
c2 = 1.496180  # Scaling co-efficient on the cognitive component
dimension = 20  # Size of the problem
iterations = 3000
swarmSize = 30


# This class contains the code of the Particles in the swarm
class Particle:
    velocity = []
    pos = []
    pBest = []
    opRep = []

    def __init__(self,dimension, mask):
        self.dimension = dimension
        for i in range(self.dimension):
            self.pos.append(random.random())
            self.velocity.append(0.01 * random.random())
            self.pBest.append(self.pos[i])
        self.opRep = converterVectorToOperation(self.pos, mask)
        return 

    def updatePositions(self):
        for i in range(self.dimension):
            self.pos[i] = self.pos[i] + self.velocity[i]
        return

    def updateVelocities(self, gBest):
        for i in range(self.dimension):
            r1 = random.random()
            r2 = random.random()
            social = c1 * r1 * (gBest[i] - self.pos[i])
            cognitive = c2 * r2 * (self.pBest[i] - self.pos[i])
            self.velocity[i] = (w * self.velocity[i]) + social + cognitive
        return

    def satisfyConstraints(self):
        # This is where constraints are satisfied
        return


# This class contains the particle swarm optimization algorithm
class ParticleSwarmOptimizer:
    solution = []
    swarm = []

    def __init__(self,dimension, mask, swarmSize=30):
        for h in range(swarmSize):
            particle = Particle(dimension, mask)
            self.swarm.append(particle)
        return

    def optimize(self):
        for i in range(iterations):
            print("iteration ", i)
            # Get the global best particle
            gBest = self.swarm[0]
            for j in range(swarmSize):
                pBest = self.swarm[j].pBest
                if self.f(pBest) and self.f(gBest):
                    gBest = pBest
            solution = gBest
            # Update position of each paricle
            for k in range(swarmSize):
                self.swarm[k].updateVelocities(gBest)
                self.swarm[k].updatePositions()
                self.swarm[k].satisfyConstraints()
            # Update the personal best positions
            for l in range(swarmSize):
                pBest = self.swarm[l].pBest
                if self.f(self.swarm[l]) and self.f(pBest):
                    self.swarm[l].pBest = self.swarm[l].pos
        return solution

    def f(self, solution):
        # This is where the metaheuristic is defined
        return random.random()


def main():
    filePath = 'instances/vorlesungsbeispiel'
    jobs = readJobs(filePath)
    m = len(jobs[0])
    j = len(jobs)
    mask = makeMask(jobs)
    pso = ParticleSwarmOptimizer(j*m,mask)
    pso.optimize()

if __name__ == '__main__':
    main()