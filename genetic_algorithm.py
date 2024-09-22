import random
import math
from config import *
from utils import fitness


def create_individual():
    return list(random.choice([0, 1]) for _ in range(len(WEIGHTS_VALUES)))



def new_population(size=POP_SIZE):
    return tuple(create_individual() for _ in range(size))

#A Taxa de mutação é de 1% e pode ser configurada
def mutate(individual, chance=MUTATION_CHANCE, chance_is_for_each=True):
    # Podemos decidir se a chance é de 1% de ALGUM BIT ter mutação ou 1% PARA CADA BIT ter mutação
    if chance_is_for_each: # Se a chance for de CADA bit ter mutação
        return list(1 - gene if random.random() < chance else gene for gene in individual)
    else: #  Se a chance for de ALGUM bit ter mutação
        if random.random() < chance: # se for menor que a chance, então
            index = random.randint(0, len(individual) - 1) #sorteia qual bit vai inverter
            return list(individual[:index] + [1 - individual[index]] + individual[index + 1:])
    return list(individual)

# definir crossover com um ou dois pontos de corte (configurável). Isso quer dizer, na hora de cruzar os números, se o bit será dividido em duas partes ou em três
def crossover(parent1, parent2, cuts=CROSSOVER_CUT_POINTS):
    if cuts == 1: # se for só com um corte, pegamos a metade de cada pai pra fazer um filho
        pivot = len(parent1) // 2
        child1 = list(parent1[:pivot] + parent2[pivot:])
        child2 = list(parent2[:pivot] + parent1[pivot:])
    elif cuts == 2: # se for com dois cortes, vamos dividir o cromossomo em tres e trocar a parte do meio
        pivot1 = len(parent1) // 3
        pivot2 = 2 * pivot1
        child1 = list(parent1[:pivot1] + parent2[pivot1:pivot2] + parent1[pivot2:])
        child2 = list(parent2[:pivot1] + parent1[pivot1:pivot2] + parent2[pivot2:])
    else:
        raise ValueError("Número de cortes não suportado")

    return mutate(child1), mutate(child2)


# A seleção é responsável por decidir quem vai cruzar
def selection(population, strategy=SELECTION_STRATEGY):
    if strategy == "ROULETTE": # na estratégia da roleta ponderada, é feito sorteio entre os indivíduos, porém a chance deles aumenta quanto melhores eles forem no fitness.
        fitnesses = [fitness(ind) for ind in population]
        _min, _max = min(fitnesses), max(fitnesses) # normalizar a fitness entre 0 e 1
        if _max != _min:
            normalized_fitnesses = [(value - _min) / (_max - _min) for value in fitnesses]
        else:
            normalized_fitnesses = [1 for _ in fitnesses]
        return random.choices(population, weights=normalized_fitnesses, k=1)[0]
    else:
        samples = random.sample(population, TOURNAMENT_SIZE)
        return max(samples, key=fitness)

# Função de reprodução para que novas gerações sejam criadas
def breed(population):
    sorted_pop = sorted(population, key=fitness, reverse=True) # Aqui ordenamos a população que será cruazada.
    survivors_count = math.ceil(ELITISM_PERCENTAGE * len(sorted_pop)) # Definimos a contagem de indivíduos sobreviventes com base na porcentagem de elitismo
    survivors = sorted_pop[:survivors_count] # Armazenamos os sobreviventes da população num array

    next_gen = list(survivors) # Criamos um vetor para a nova geração começando com os sobreviventes, o tamanho será 0 caso a porcentagem de elitismo seja 0
    while len(next_gen) < len(population): # Enquanto a população da nova geração for menor que a geração antiga
        parent1, parent2 = selection(population), selection(population) # Selecionamos os pais
        child1, child2 = crossover(parent1, parent2) # Criamos os filhos fazendo crossover com os pais selecionados
        next_gen.extend([child1, child2]) # Filhos são adicionados na nova geração

    return tuple(next_gen[:len(population)])

# Função de evolução
def evolve(population, steps=1):
    for _ in range(steps):
        population = breed(population)
    return population