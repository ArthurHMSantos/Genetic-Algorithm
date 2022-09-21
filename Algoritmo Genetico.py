from random import choice, randint


# create class Address
class Address:
    def __init__(self, letter, tuple_coordinate):
        self.letter = letter
        self.tuple_coordinate = tuple_coordinate


r = Address("R", (0, 0))  # default position for R is 0, 0


# all functions

# address the matrix letters and their correspondent coordinates to the class Address
def create_matrix_coordinates(table):
    aux = []
    count = 0
    for row_index, item in enumerate(table):
        row = table[row_index].split()
        for column_index in range(len(row)):
            if row[column_index] == 'R':
                r.tuple_coordinate = (row_index, column_index)
            elif row[column_index] != '0':
                aux.append(Address(row[column_index], (row_index, column_index)))
                count += 1
    return aux, count


# create a random path from the list of coordinates given and assures there's no repetition
def generate_random_path(coordinates_list, pill):
    pop_inicial = []
    while True:
        rand = choice(coordinates_list)
        if rand not in pop_inicial:
            pop_inicial.append(rand)
        elif len(pop_inicial) == len(coordinates_list):
            pop_inicial.insert(0, r)
            pop_inicial.append(r)
            break
    if pop_inicial not in pill:
        return pop_inicial


# create the first population of paths
def generate_inicial_pop(informed_list):
    pill = []
    while True:
        pill.append(generate_random_path(informed_list, pill))
        if pill[-1] is None:
            pill.pop()

        if len(informed_list) > 5 and len(pill) == 400:  # for more than 5 coordinates
            return pill


# partially met crossover; do the crossover
def pmx(gen):
    next_gen = []
    for index in range(0, len(gen), 2):

        # first two sons
        father_one = gen[index].copy()
        father_two = gen[index + 1].copy()
        remove_r(father_one, father_two)
        father_one_copy, father_two_copy = father_one.copy(), father_two.copy()

        crossover_cut = randint(1, len(father_one) - 1)

        for cut in range(crossover_cut):
            for char in range(len(father_one_copy)):
                if father_two[cut] == father_one[char]:
                    father_one_copy[cut], father_one_copy[char] = father_one_copy[char], father_one_copy[cut]

                if father_one[cut] == father_two[char]:
                    father_two_copy[cut], father_two_copy[char] = father_two_copy[char], father_two_copy[cut]

        first_son, second_son = add_r(father_one_copy, father_two_copy)
        next_gen.append(first_son)
        next_gen.append(second_son)
        # latter two sons
        father_one = gen[index].copy()
        father_two = gen[index + 1].copy()
        remove_r(father_one, father_two)
        father_one_copy, father_two_copy = father_one.copy(), father_two.copy()

        crossover_cut = randint(1, len(father_one) - 1)

        for cut in range(crossover_cut):
            for char in range(len(father_one_copy)):
                if father_two[cut] == father_one[char]:
                    father_one_copy[cut], father_one_copy[char] = father_one_copy[char], father_one_copy[cut]

                if father_one[cut] == father_two[char]:
                    father_two_copy[cut], father_two_copy[char] = father_two_copy[char], father_two_copy[cut]

        first_son, second_son = add_r(father_one_copy, father_two_copy)
        next_gen.append(first_son)
        next_gen.append(second_son)
    return next_gen


# remove r from a couple of fathers
def remove_r(first_father, second_father):
    first_father.remove(r)
    first_father.pop()
    second_father.remove(r)
    second_father.pop()
    return first_father, second_father


# add r to a couple of fathers
def add_r(first_son, second_son):
    first_son.append(r)
    first_son.insert(0, r)
    second_son.append(r)
    second_son.insert(0, r)
    return first_son, second_son


# calculates the distance for one path
def get_distance_list_from_coordinates(address_sequence):
    temp = []

    for i in range(len(address_sequence) - 1):
        first_tuple = address_sequence[i].tuple_coordinate
        second_tuple = address_sequence[i + 1].tuple_coordinate

        d1 = abs(first_tuple[0] - second_tuple[0])
        d2 = abs(first_tuple[1] - second_tuple[1])
        distance_result = (d1 + d2)
        temp.append(distance_result)
    return temp


# get a list with all the paths distance
def get_total_distance(informed_distance_list):
    total = 0
    for distance in informed_distance_list:
        total += distance
    return total


# return the list of all results
def result_list(population):
    total_results_list = []
    for sequence in population:
        distance_list = get_distance_list_from_coordinates(sequence)
        result = get_total_distance(distance_list)
        total_results_list.append(result)
    return total_results_list


# verify the index of the path with minimum distance
def min_distance_index(list_of_paths):
    minimum_distance_index = 0
    for distance_index in range(len(list_of_paths)):
        if list_of_paths[distance_index] < list_of_paths[minimum_distance_index]:
            minimum_distance_index = distance_index
    return minimum_distance_index


# rearranges the list index to better understanding
def show(informed_list, min_index):
    minimum = ""
    for address in informed_list[min_index]:
        minimum += str(address.letter)
    return minimum


# sort the population in crescent order of paths distances
def sort_pop(original_pop, switch):
    college = []
    population_copy = original_pop.copy()
    while True:
        for _ in range(len(population_copy)):
            result_list_copy = result_list(population_copy)
            min_index = min_distance_index(result_list_copy)
            college.append(population_copy[min_index])
            if len(college) >= 100 and switch == 0:
                return college
            elif switch == 1 and len(college) == 3:
                return college
            elif switch == 2 and len(college) == 5:
                return college
            population_copy.remove(population_copy[min_index])


# mutate the population
def mutation(cell):
    for index in range(0, len(cell)):
        mut = randint(1, 100)  # percentage of mutation (5%)
        if mut <= 5:
            cell[index].remove(r)
            cell[index].pop()
            change = randint(1, len(cell[index]) - 1)
            cell[index][change], cell[index][len(cell[index]) - change - 1] = cell[index][
                                                                                  len(cell[index]) - change - 1], \
                                                                              cell[index][change]
            cell[index].append(r)
            cell[index].insert(0, r)
    return cell


# create an elite of the 3 best in each gen
def elitism(original_pop):
    elit = sort_pop(original_pop, 1)
    common = sort_pop(original_pop, 0)
    return sort_pop(common[:len(common) - 3] + elit, 0)


# runs the genetic algorithm
def alg_gen(informed_population):
    terminator = 0
    for c in range(100):
        informed_population = elitism(mutation(pmx(informed_population)))
        if informed_population[0] == informed_population[-1]:
            terminator += 1
            if terminator >= 2:
                print("Em andamento...")
                return informed_population[0]


# permutation for brute force
def permute_list(informed_list):
    if len(informed_list) == 0:
        return []
    if len(informed_list) == 1:
        return [informed_list]

    aux = []
    for index in range(len(informed_list)):
        chain = informed_list[index]
        remix = informed_list[:index] + informed_list[index + 1:]

        for unchained in permute_list(remix):
            aux.append([chain] + unchained)
    return aux


# code


def main():
    matriz = open('Entrada.txt')
    matrix = matriz.readlines()
    address_set, counter = create_matrix_coordinates(matrix)  # creates initial coordinates list
    if len(address_set) >= 6:  # if there's more than 5 relevant points in the matrix do genetic algorithm
        initial_pop = generate_inicial_pop(address_set)  # generate initial population
        sorted_initial_pop = sort_pop(initial_pop, 0)  # evaluate the initial population

        # crossing over and repeating the genetic algorithm
        new_pop = elitism(mutation(pmx(sorted_initial_pop)))  # crossover evaluated pop -> do mutation -> elite of 3
        pop = []
        for samples in range(5):
            pop.append(alg_gen(
                new_pop))  # runs the entire genetic algorithm 10 times and keep the best rest results of each "batch"
            print(f"Resultado {samples + 1} finalizado!")

        # final evaluation
        sorted_final_list = sort_pop(pop, 2)

        print("Escolhendo melhor resultado...")
        print("Feito!")
        print(
            f"O menor caminho encontrado foi: {show(sorted_final_list, 0)} com distancia {result_list(sorted_final_list)[0]}")
    else:  # if there's less than 5 relevant points in the matrix do brute force
        # permutation of address_set points
        permuted_list = permute_list(address_set)
        for permutation in permuted_list:
            permutation.insert(0, r)
            permutation.append(r)

        results_list = []
        # do math and takes the shortest path
        for sequence in permuted_list:
            distance_list = get_distance_list_from_coordinates(sequence)
            result = get_total_distance(distance_list)
            results_list.append(result)
        min_index = (min_distance_index(results_list))

        print(
            f"O menor caminho encontrado foi: {show(permuted_list, min_index)}, com distancia {results_list[min_index]}")


if __name__ == "__main__":
    main()
