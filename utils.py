from config import WEIGHT_LIMIT, WEIGHTS_VALUES


def fitness(x):
    if(get_total_weight(x, WEIGHTS_VALUES) > WEIGHT_LIMIT):
        return 0
    else:
        return get_total_value(x, WEIGHTS_VALUES)

def get_total_weight(individual, weight_list):
    if len(individual) != len(weight_list):
        raise Exception("Individual and weight_list must have the same length")

    total_weight = 0
    for i in range(len(individual)):
        if individual[i] == 1:
            total_weight += weight_list[i][0]

    return total_weight

def get_total_value(individual, weight_list):
    if len(individual) != len(weight_list):
        raise Exception("Individual and weight_list must have the same length")

    total_value = 0
    for i in range(len(individual)):
        if individual[i] == 1:
            total_value += weight_list[i][1]

    return total_value
