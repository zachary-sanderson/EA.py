from random import choice, random, randint
from copy import deepcopy

### EVOLUTIONARY ALGORITHM ###

def evolve(filename):
    grid = checkGrid(filename)
    population = create_pop(grid)
    fitness_population = evaluate_pop(population)
    prev_best_ind = []
    best_ind = []
    same_best = 0
    best_gen = 100
    solution_found = False
    for gen in range(NUMBER_GENERATION):
        mating_pool = select_pop(population, fitness_population)
        offspring_population = crossover_pop(mating_pool)
        if prev_best_ind == best_ind:
            same_best += 1
        else:
            same_best = 0
        if same_best > 2:
            population = mutate_pop2(offspring_population, filename)
        else:
            population = mutate_pop(offspring_population, filename)
        prev_best_ind = best_ind
        fitness_population = evaluate_pop(population)
        best_ind, best_fit = best_pop(population, fitness_population)
        if best_fit < best_gen:
            best_gen = best_fit
        print("#%3d" % gen, "fit:%3d" % best_fit)
        print("best individual:")
        for row in best_ind:
            print(row)
        if best_ind == 0:
            solution_found = True
            break
    if solution_found:
        print("Solution found!")
    else:
        print("Unsolved! Best Fit = ", best_gen)

### POPULATION-LEVEL OPERATORS ###

def create_pop(grid):
    return [ create_ind(deepcopy(grid)) for _ in range(POPULATION_SIZE) ]

def evaluate_pop(population):
    return [ evaluate_ind(individual) for individual in population ]

def select_pop(population, fitness_population):
    sorted_population = sorted(zip(population, fitness_population), key = lambda ind_fit: ind_fit[1])
    return [ individual for individual, fitness in sorted_population[:int(POPULATION_SIZE * TRUNCATION_RATE)] ]

def crossover_pop(population):
    return [ crossover_ind(choice(population), choice(population)) for _ in range(POPULATION_SIZE) ]

def mutate_pop(population, filename):
    return [ mutate_ind(individual, checkGrid(filename)) for individual in population ]

def mutate_pop2(population, filename):
    return [ mutate_ind2(individual, checkGrid(filename)) for individual in population ]


def best_pop(population, fitness_population):
    return sorted(zip(population, fitness_population), key = lambda ind_fit: ind_fit[1])[0]

### INDIVIDUAL-LEVEL OPERATORS: REPRESENTATION & PROBLEM SPECIFIC ###

def checkGrid(filename):
    with open(filename) as file:
        lines = [(line.rstrip('\n')).strip('') for line in file]
        rows = []
        row = []
        ints = [str(num) for num in range(1,10)]
        for line in lines:
            for elem in list(line):
                if elem == '-' or elem == '!':
                    continue
                if len(row) == 9:
                    rows.append(row)
                    row = []
                if elem in ints:
                    row.append(int(elem))
                else:
                    row.append(elem)
        rows.append(row)
    return rows
				
def evaluate_ind(ind):
    columns = get_columns(ind)
    boxes = get_boxes(ind)

    return fitnessVal(columns, boxes)
			
def fitnessVal(columns, boxes):
    fitness = 0
    for i in range(gridsize):
        col_nums = []
        box_nums = []
        for j in range(gridsize):
            if columns[i][j] not in col_nums:
                col_nums.append(columns[i][j])
            else:
                fitness += 1
            if boxes[i][j] not in box_nums:
                box_nums.append(boxes[i][j])
            else:
                fitness += 1
        
    return fitness
	
def create_ind(grid):
    possible_vals = []
    for num in nums:
        possible_vals = possible_vals + [num]*9
    for row in grid:
        for num in row:
            if num != '.':
                possible_vals.remove(int(num))
    for row in grid:
        i = 0
        while i < 9:
            if row[i] == '.':
                row_choices = [n for n in nums if n not in row]
                column = []
                boxes = get_boxes(grid)
                n = grid.index(row)
                if n < 3:
                    if i < 3:
                        box_choices = [n for n in nums if n not in boxes[0]]
                    elif i < 6:
                        box_choices = [n for n in nums if n not in boxes[1]]
                    else:
                        box_choices = [n for n in nums if n not in boxes[2]]
                if n < 6:
                    if i < 3:
                        box_choices = [n for n in nums if n not in boxes[3]]
                    elif i < 6:
                        box_choices = [n for n in nums if n not in boxes[4]]
                    else:
                        box_choices = [n for n in nums if n not in boxes[5]]
                else:
                    if i < 3:
                        box_choices = [n for n in nums if n not in boxes[6]]
                    elif i < 6:
                        box_choices = [n for n in nums if n not in boxes[7]]
                    else:
                        box_choices = [n for n in nums if n not in boxes[8]]
                for j in range(9):
                    column.append(grid[j][i])
                choices = list(set(row_choices) - set(column) - set(box_choices))
                if choices == []:
                    new_vals = [n for n in nums if n not in possible_vals]
                    choices = list(set(row_choices) - set(new_vals))
                    if choices == []:
                        elem = choice(possible_vals)
                    else:
                        elem = choice(choices)
                else:
                    elem = choice(choices)
                row[i] = elem
                possible_vals.remove(elem)
                
            else :
                row[i] = int(row[i])
             
            i = i + 1
    return grid
	
def mutate_ind(individual,grid):
    for i in range(len(individual)):
        choices = [n for n in nums if n not in grid[i]]
        if random() < MUTATION_RATE:
            index1 = individual[i].index(choice(choices))
            choices.remove(individual[i][index1])
            index2 = individual[i].index(choice(choices))
            individual[i][index1], individual[i][index2] = individual[i][index2], individual[i][index1]
            cols = get_columns(individual)
            if len(set(cols[index1])) + len(set(cols[index2])) != 18:
                individual[i][index1], individual[i][index2] = individual[i][index2], individual[i][index1]
    return individual

def mutate_ind2(individual,grid):
    for i in range(len(individual)):
        choices = [n for n in nums if n not in grid[i]]
        if random() < MUTATION_RATE:
            index1 = individual[i].index(choice(choices))
            choices.remove(individual[i][index1])
            index2 = individual[i].index(choice(choices))
            individual[i][index1], individual[i][index2] = individual[i][index2], individual[i][index1]
            cols = get_columns(individual)
            if len(set(cols[index1])) + len(set(cols[index2])) < 16:
                individual[i][index1], individual[i][index2] = individual[i][index2], individual[i][index1]
    return individual

def get_columns(ind):
    columns = []
    column = []
    for i in range(gridsize):
        column = []
        for row in ind:
            column.append(row[i])
        columns.append(column)
    return columns
                
def get_boxes(ind):
    boxes = []
    for i in range(0,gridsize,3):
        box = []
        for j in range(9):
            three = [ind[j][i], ind[j][i+1], ind[j][i+2]]
            box = box + three
            if (j+1) % 3 == 0:
                boxes.append(box)
                box = []
    return boxes
	
def crossover_ind(individual1, individual2):
    crossover_point1 = randint(0, 8)
    crossover_point2 = randint(1, 9)
    while(crossover_point1 == crossover_point2):
        crossover_point1 = randint(0, 8)
        crossover_point2 = randint(1, 9)
                
    if(crossover_point1 > crossover_point2):
        temp = crossover_point1
        crossover_point1 = crossover_point2
        crossover_point2 = temp
                
    for i in range(crossover_point1, crossover_point2):
        individual1[i], individual2[i] = individual2[i], individual1[i]
        
    if evaluate_ind(individual1) > evaluate_ind(individual2):
        if random() < 0.8:
            return individual2
        else:
            return individual1
    else:
        if random() < 0.8:
            return individual1
        else:
            return individual2


### PARAMATERERS VALUES ###
nums = range(1,10)
gridsize = len(nums)

NUMBER_GENERATION = 100
POPULATION_SIZE = 100
TRUNCATION_RATE = 0.5
MUTATION_RATE = 1.0 / 20

evolve("Grid1.txt")
evolve("Grid2.txt")
evolve("Grid3.txt")


