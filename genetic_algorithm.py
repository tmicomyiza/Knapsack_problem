from termcolor import colored
import random
import math


######################################################################################
#                                                                                    #
# CONSTANT VARIABLES THAT WILL BE USED AND WON'T CHANGE WHILE THE PROGRAM IS RUNNING #
#                                                                                    #
#       1. MAX WEIGHT OF THE BACKPACK                                                #
#       2. MAX NUMBER OF GENERATIONS                                                 #
#       3. POPULATION  SIZE                                                          #
######################################################################################

MAX_WEIGHT      = 250
MAX_GENERATION  = 50
POPULATION_SIZE = 20




#######################################################################
#                                                                     #
#                 CLASS THAT REPRESENTS A BOX                         #
#                                                                     #
#######################################################################

class Box():
    def __init__(self, weight, value, status):
        self.weight = weight
        self.value  = value
        self.status = status







#############################################################################
#                                                                           #
#      FUNCTIONS TO IMPLEMENT THE ALGORITHM                                 #
#                                                                           #
#############################################################################



'''
Parameters: chromosome: list of boxes
'''
def mutation(chromosome):
    # randomly select a box to change its status
    index = random.randint(0, len(chromosome) - 1)

    if chromosome[index].status == 0:
        chromosome[index].status = 1
    
    else:
        chromosome[index].status = 0


    return chromosome

'''
Parameters: 
            population : list of chromosomes

Returns:
            shorter population which is 1/2 of original list
'''
def select_fittest(population):

    # sort the population in ascending order based on fitness
    population = sorted(population, key=lambda x: fitness(x), reverse=True)



    length = len(population)
    # remove half of population with lowest fitness
    for i in range(length // 2):
        population.pop()

    # return updated population
    return population




'''
Parameters: 
            2 chromosomes to crossover

Returns: 
            a new chromsome
'''
def crossover(parent_1, parent_2):
    
    # randomly select a pivot to crossover from
    pivot = random.randint(1,len(parent_1) - 1)
    new_chromosome = list()

    # get the first part of the new_chromosome from parent_1
    for i in range(pivot):
        new_chromosome.append(parent_1[i])


    # second part will come from parent_2
    for i in range(pivot, len(parent_1)):
        new_chromosome.append(parent_2[i])

    # return the new generated chromosome: list of boxes that can possibly be a solution
    return new_chromosome



'''
Parameters: 
            1. chromosome: list of boxes
            2. max_weight: int representing maximum limit of container

Returns:    it returns positive value representing fitness of the chromosome
            otherwise it returns 0 if weight is greater than max_weight. 

Formula : fitness of a chromosome if the sum of v_i * status_i
'''
def fitness(chromosome):

    sum_weights = 0
    sum_values = 0

    for box in chromosome:
        sum_weights += box.status * box.weight
        sum_values += box.status * box.value

    if sum_weights > MAX_WEIGHT:
        # the chromosome is oversized, thus cannot be a solution
        return 0
    
    else:
        # valid size which is below the maximum capacity of the holder
        return sum_values
    
    

'''
Parameters: 
            1. Population 
            2. int value representing which generation we are currently processing
            3. filename to write result to

Does    :  writes generation information on a file provided
'''    

def pretty_print(population, generation, filename):
    filename.write("Generation #" + str(generation) + "\n")
    filename.write("[ \n")

    for item in population:
        filename.write("[")

        count = 0
        for index in item:

            if count < len(item) - 1:
                filename.write(str(index.status) + ", ")

            else:
                filename.write(str(index.status))

            count += 1

        filename.write("] \n")

    filename.write("] \n")




'''
Parameters:
            individual : a chromosome or list of boxes


Does      : prints the results in a preferred format on the terminal
'''

def print_solution(individual):
    print(colored("FINAL SOLUTION", "blue"))
    print(colored("Boxes to pack identified by index (1 -> n)", "blue"))

    print(colored("NUMBER   WEIGHT   VALUE", "blue"))
    print(colored("==========================", "blue"))
    index = 0
    total_weight = 0
    for item in individual:
        if item.status == 1:
            print(colored("   {} ".format(index + 1),"blue"), end = "   ")
            print(colored(" {} ".format(item.weight), "blue"), end= "   ")
            print(colored(" {}".format(item.value), "blue"))

            total_weight += item.weight
        index += 1

    print(colored("Fitness is {}".format(fitness(individual)), "blue"))
    print(colored("Total Weight is {}".format(total_weight), "blue"))





'''
Parameters: 
            Population which is half size of original population

Returns:   Population of same size as original which is generated using crossover
            operation
'''
def next_generation(population):

    length = len(population) - 1
    for i in range (POPULATION_SIZE // 2):
        parent_1 = population[random.randint(0, length)]
        parent_2 = population[random.randint(0, length)]

        new_chromosome = crossover(parent_1, parent_2)
        
        # probability whether child should be mutated or not
        mutate = random.randint(0,3)
        if mutate == 1:
            new_chromosome = mutation(new_chromosome)

        population.append(new_chromosome)


    return population






'''
Parameters:
            Population to be processed


Returns: nothing

Does    : Implements genetic algorithm 
'''
def genetic_algorithm(population):

    filename = open("generations.txt", "w+")
    for g in range(MAX_GENERATION):
        pretty_print(population, g + 1,filename)

        # select the fittest from a population will return 1/2 of original population
        population = select_fittest(population)

        # create next generation using crossover to fill the next 1/2 of population
        population = next_generation(population)



    solution = sorted(population, key=lambda x: fitness(x), reverse=True)[0]

    # in case there is no solution
    if fitness(solution) == 0:
        print(colored("Sorry! NO SOLUTION FOUND","red"))
        return


    print_solution(solution)
    filename.close()

    



'''
Parameters: 
            boxes: list of box objects


Returns  : a population: list of chromosomes

'''
def init_population(boxes):
    population = []
    # initializes population 
    # each chromosome is a list of length num_boxes with each element assigned to status of 0 or 1
    for i in range (POPULATION_SIZE):
        chromosome = []
        for j in range (len(boxes)):
            value  = boxes[j].value
            weight = boxes[j].weight
            
            chromosome.append(Box(weight, value, random.randint(0,1)))
        
        population.append(chromosome)



    return population



'''
Parameters: None

Does      : it is used when user wants to provide box values instead of
            using randomly generated values
'''
def provided():
    num_boxes = int(input(colored("how many boxes do you want to pack? ", "green")))

    set_boxes = []

    # read in box info from the terminal
    for i in range(num_boxes):
        data = input(colored ("Enter the size of the box and value separated by a space: ", "green")).split()
        box = Box(int(data[0]), int(data[1]), 0)
        set_boxes.append(box)

    # generate initial population
    population = init_population(set_boxes)

    # implement the algorithm provided the generated population
    genetic_algorithm(population)



'''
Parameters: None

Does      : is used when user chooses the program to randomly generate box information

'''

def randomised():

    num_boxes = random.randint(3, 10)   #number of boxes we want to pack

    set_boxes = []

    # generate boxes with their corresponidng weight and value
    for i in range(num_boxes):
        box = Box(random.randint(30, 100), random.randint(1,250), 0)
        set_boxes.append(box)


    # generate initial population
    population = init_population(set_boxes)


    #implement the algorithm
    genetic_algorithm(population)






if __name__ == "__main__":
    choice = input(colored("Do you want to provide boxes and values? (y/n): ","green"))

    if choice.upper() == "Y":
        provided()
    
    elif choice.upper() == "N":
        randomised()

    else:
        print(colored("Error: Invalid input {}".format(choice),"red"))