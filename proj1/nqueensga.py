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
        neighbour = BoardState(self.pS, board=newBoard)
        return neighbour

def initializePopulation(bS, pS, popSize):
    population = []
    repaired = repair(bS.board)
    bS = BoardState(pS, board=repaired)
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
    """
    Order1 crossover with population diversifying
    """
    switches = random.sample(range(pS.size+1), 2)
    switches.sort()
    cb = p2.board[:]
    if p1.board == p2.board:
        random.shuffle(cb)
    for col in p1.board[switches[0]:switches[1]]:
        remove = -1
        for i in range(len(cb)):
            if cb[i] == col:
                remove = i
        del cb[remove]
    ncb = cb[:switches[0]]
    ncb.extend(p1.board[switches[0]:switches[1]])
    ncb.extend(cb[switches[0]:])
    child = BoardState(pS, board=ncb)
    return child

def tournament(population, solutions, pS):
    """
    Runs tournament on three random individuals.
    Worst individual is killed and replaced with
    reproduction result from the others.
    """
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
    if random.random() < 0.10:
        population[kill] = population[parent[0]].mutate()
    else:
        population[kill] = crossover(population[tourney[0]], population[tourney[1]], pS)
    if random.random() < 0.02:
        population[kill] = population[kill].mutate()
    if population[kill].energy == pS.target:
        solutions.add(tuple(population[kill].board))
        derivates = expandSolution(population[kill].board)
        for solution in derivates:
            solutions.add(tuple(solution))

def nuclearAccident(population, solutions, pS):
    """
    Mutates the entire population to a small degree,
    to keep it diversified.
    """
    for i in range(len(population)):
        population[i] = population[i].mutate()
        if random.random() < 0.50:
            population[i] = population[i].mutate()
        if population[i].energy == pS.target:
            solutions.add(tuple(population[i].board))
            derivates = expandSolution(population[i].board)
            for solution in derivates:
                solutions.add(tuple(solution))

def nQueensGenAlg(initPop, pS, itr, nuclearSafetyBudget, steps):
    population = initPop
    solutions = set([])
    for i in range(itr):
        tournament(population, solutions, pS)
        if i % nuclearSafetyBudget == 0:
            nuclearAccident(population, solutions, pS)
        print(len(solutions), end='\r')
    return solutions

def main():
    steps = askForStep()
    #startBoard = getInput()
    startBoard = [0 for i in range(30)]
    startBoard = repair(startBoard)
    
    pS = ProblemState(len(startBoard))
    bS = BoardState(pS, board=startBoard)
    initPop = initializePopulation(bS, pS, 1000)

    start = time.clock()
    solutions = nQueensGenAlg(initPop, pS, 1200000, 300000, steps)
    end = time.clock()

    printSolutions(solutions)
    printRuntime(end - start)

if __name__ == '__main__':
    main()
