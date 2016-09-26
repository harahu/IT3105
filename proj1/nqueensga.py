import random, time
from tools import *


class BoardState():
    def __init__(self, pS, **kwargs):
        self.pS = pS
        self.board = kwargs.get('board')
        if self.board is not None:
            self.locationStates();
            self.energy()
            self.req = 0

    def locationStates(self):
        """Returns a lookup table for number of queens in a given diagonal"""
        self.locStates = [[0 for i in range(2 * self.pS.size - 1)], [0 for i in range(2 * self.pS.size - 1)]]
        for col in range(self.pS.size):
            row = self.board[col]
            #marking NW to SE diagonal as under attack
            self.locStates[0][self.pS.diagCoords[col][row][0]] += 1
            #marking SW to NE diagonal as under attack
            self.locStates[1][self.pS.diagCoords[col][row][1]] += 1

    def energy(self):
        self.energy = self.pS.target
        for locList in self.locStates:
            for line in locList:
                    self.energy -= self.pS.comb[line]

    def mutate(self):
        cols = random.sample(range(self.pS.size), 2)
        newBoard = self.board[:]
        newBoard[cols[0]] = self.board[cols[1]]
        newBoard[cols[1]] = self.board[cols[0]]
        neighbour = boardState(self.pS, board=newBoard)
        return neighbour

def initializePopulation(bS, pS, popSize):
    population = []
    repaired = repair(bS.board)
    bS = boardState(pS, board=repaired)
    population.append(bS)
    for i in range(popSize-1):
        derivative = bS.mutate().mutate()
        population.append(derivative)
    return population

def rouletteWheelSelection(population, pointers):
    keep = []
    for p in pointers:
        i = 0
        fSum = population[0].energy
        while fSum < p:
            i += 1
            fSum+=population[i].energy
        keep.append(population[i])
    return keep


def stocasticUniversalSampling(population, n):
    f = 0
    for individual in population:
        f += individual.energy
    pD = f//n
    sP = random.randint(0, pD)
    pointers = [(sP + i*pD) for i in range(n-1)]
    return rouletteWheelSelection(population, pointers)

def crossover(p1, p2, pS):
    switches = random.sample(range(pS.size), 2)
    switches.sort()
    cb = p1.board[:switches[0]]
    cb.extend(p2.board[switches[0]:switches[1]])
    cb.extend(p1.board[switches[1]:])
    cb = repair(cb)
    child = boardState(pS, board=cb)
    return child

"""
def crossover(p1, p2, pS):
    cb = [i for i in range(pS.size)]
    random.shuffle(cb)
    for i in range(pS.size):
        if p1.board[i] == p2.board[i]:
            for j in range(pS.size):
                if cb[j] == p1.board[i]:
                    cb[j] = cb[i]
                    cb[i] = p1.board[i]
    child = boardState(pS, board=cb)
    return child
"""

def reproduce(parents, n, crossRate, mutationRate, pS):
    children = []
    for i in range(n):
        parent = parents[(i % len(parents))]
        if random.random() <= crossRate:
            randParent = parents[random.randint(0, len(parents)-1)]
            child = crossover(parent, randParent, pS)
        else:
            child = parent
        if random.random() < mutationRate:
            child = child.mutate()
        children.append(child)
    return children

def tourney(pop):
    best = None
    maxEng = 0
    for bS in pop:
        if bS.energy > maxEng:
            best = bS
            maxEng = bS.energy
    return best


def nQueensGenAlg(initPop, pS, itr):
    population = initPop
    solutions = set([])
    for i in range(itr):
        kill = -1
        low = pS.target
        tourney = random.sample(range(len(population)),  3)
        tC = -1
        for j in range(len(tourney)):
            if population[tourney[j]].energy < low:
                kill = tourney[j]
                low = population[tourney[j]].energy
                tC = j
        del tourney[tC]
        parent = random.sample(tourney, 1)
        if random.random() < 0.99:
            population[kill] = population[parent[0]].mutate()
        else:
            population[kill] = crossover(population[tourney[0]], population[tourney[1]], pS)
        if random.random() < 0.02:
            population[kill] = population[kill].mutate()
        if population[kill].energy == pS.target:
                solutions.add(tuple(population[kill].board))
                print(str(len(solutions))+" "+str(i))
        #reactor meltdown
        
        if i % 50000 == 0:
            for j in range(len(population)):
                population[j] = population[j].mutate()
                if random.random() < 0.50:
                    population[j] = population[j].mutate()
                if population[j].energy == pS.target:
                    solutions.add(tuple(population[j].board))
                    print(str(len(solutions))+" "+str(i))
        
    return solutions

def main():
    inBoard = [i for i in range(30)]
    pS = ProblemState(len(inBoard))
    bS = BoardState(pS, board=inBoard)
    initPop = initializePopulation(bS, pS, 100)
    start = time.clock()
    solutions = nQueensGenAlg(initPop, pS, 1000000)
    end = time.clock()
    print(len(solutions))
    print("Runtime: "+str(end - start)+" seconds\n")

if __name__ == '__main__':
    main()
