def nQueensGenAlg(pS, bS, iterations):
    population = []
    for i in range(iterations):
        parents = chooseParents(population)
        children = mutate(reproduce(parents))
        population = selectFromPopulations(parents, children)

def main():


if __name__ == '__main__':
    main()
