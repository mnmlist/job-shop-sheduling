import jobshop
import random

w = 0.729844  # Inertia weight to prevent velocities becoming too large
c1 = 1.496180  # Scaling co-efficient on the social component
c2 = 1.496180  # Scaling co-efficient on the cognitive component
dimension = 20  # Size of the problem
iterations = 3000 # Number of itterations
swarmSize = 30 # Size of the swarm


# This class contains the code of the Particles in the swarm
class Particle:
    def __init__(self,dimension, mask, jobs):
        self.velocity = []
        self.pos = []
        self.posBest = [] # store best position for particle
        self.posRep = [] # store vector representation in schedule
        self.dimension = dimension
        self.jobs = jobs
        self.mask = mask
        for i in range(self.dimension):
            self.pos.append(random.random())
            self.velocity.append(0.01 * random.random())
            self.posBest.append(self.pos[i])
        self.updatePosRep()
        self.updatePosBestRep()
        self.updateCost()
        return

    def updatePosRep(self):
        """
        update position representation
        """
        self.posRep = jobshop.converterVectorToOperation(self.pos, self.mask)

    def updatePosBestRep(self):
        """
        update best position representation
        """
        self.posBestRep = jobshop.converterVectorToOperation(self.pos, self.mask)

    def updatePositions(self):
        """
        update position
        """
        for i in range(self.dimension):
            self.pos[i] = self.pos[i] + self.velocity[i]
        return

    def updateVelocities(self, gBest):
        """
        update velocity
        """
        for i in range(self.dimension):
            r1 = random.random()
            r2 = random.random()
            social = c1 * r1 * (gBest.pos[i] - self.pos[i])
            cognitive = c2 * r2 * (self.posBest[i] - self.pos[i])
            self.velocity[i] = (w * self.velocity[i]) + social + cognitive
        return

    def updateCost(self):
        """
        update cost
        """
        self.cost = jobshop.cost(self.jobs, self.posRep)


# This class contains the particle swarm optimization algorithm
class ParticleSwarmOptimizer:
    solution = []
    swarm = []

    def __init__(self,dimension, mask,jobs, swarmSize=30):
        self.jobs = jobs
        for h in range(swarmSize):
            particle = Particle(dimension, mask, jobs)
            self.swarm.append(particle)
        return

    def optimize(self):
        for i in range(iterations):
            print("iteration ", i)

            # Get the global best particle
            gBest = self.swarm[0]
            for j in range(swarmSize):
                tempParticle = self.swarm[j]
                if self.f(gBest.posRep) > self.f(tempParticle.posRep):
                    gBest = tempParticle
            solution = gBest

            # Update position of each paricle
            for k in range(swarmSize):
                self.swarm[k].updateVelocities(gBest)
                self.swarm[k].updatePositions()
                self.swarm[k].satisfyConstraints()
                self.swarm[k].updatePosRep()
                self.swarm[k].updatePosBestRep()
                self.swarm[k].updateCost()


            # Update the personal best positions
            for l in range(swarmSize):
                if self.f(self.swarm[l].posBestRep) < self.f(self.swarm[l].posRep):
                    self.swarm[l].posBest = self.swarm[l].pos
                    self.swarm[l].updatePosBestRep()

        return solution

    def f(self, solution):
        return jobshop.cost(self.jobs, solution)

