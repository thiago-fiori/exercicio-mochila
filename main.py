from config import POP_SIZE, MAX_GENERATIONS, WEIGHTS_VALUES
from genetic_algorithm import new_population, evolve
from utils import get_total_value, get_total_weight, fitness


def main():
    population_history = []

    start_pop = new_population(POP_SIZE)
    population_history.append(start_pop)

    current_pop = start_pop
    for gen in range(MAX_GENERATIONS):
        current_pop = evolve(current_pop)  # Evolve for one generation
        population_history.append(current_pop)
        best = sorted(current_pop, key = lambda i: fitness(i))[-1]

        print(f"Generation {gen + 1}:")
        print(f"Melhor indivíduo: {best} {get_total_value(best, WEIGHTS_VALUES)} {get_total_weight(best, WEIGHTS_VALUES)}")


if __name__ == "__main__":
    main()