import random
import operator
import numpy as np
from deap import base, creator, tools, gp
from src.primitivas.representacion import setup_gp_pset  # O donde hayas puesto setup_gp_pset
from src.backtest.fitness import evaluar_estrategia_trading

def run_genetic_pipeline(df_master, n_generations=10, pop_size=50):
    """
    Orquesta el motor de Programación Genética usando DEAP.
    """
    print("Inicializando el conjunto de primitivas (Terminales y Funciones)...")
    pset = setup_gp_pset()

    # 1. Configurar tipos de DEAP (Maximizar el Ratio de Sharpe -> peso = 1.0)
    if not hasattr(creator, "FitnessMax"):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    if not hasattr(creator, "Individual"):
        creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()

    # 2. Generadores de árboles (Grow / Full / Half-and-Half) con profundidad 2 a 5
    toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=2, max_=5)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # 3. Registrar función de evaluación (Fitness)
    toolbox.register("evaluate", evaluar_estrategia_trading, pset=pset, df_master=df_master)

    # 4. Operadores genéticos
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr, pset=pset)

    # Limitador de tamaño de árboles (Bloat control: profundidad máxima = 6)
    toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=6))
    toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=6))

    print(f"Generando población inicial (Tamaño: {pop_size})...")
    population = toolbox.population(n=pop_size)
    hall_of_fame = tools.HallOfFame(1)  # Guarda el mejor individuo de todo el proceso

    # Estadísticas para monitorizar la evolución
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("max", np.max)
    stats.register("min", np.min)

    print(f"Lanzando el bucle evolutivo ({n_generations} generaciones)...")
    
    # Evaluación inicial de la población
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    hall_of_fame.update(population)

    for gen in range(1, n_generations + 1):
        # Selección de la siguiente generación
        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))

        # Aplicar cruce y mutación (Crossover & Mutation)
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < 0.7:  # Probabilidad de cruce
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < 0.2:  # Probabilidad de mutación
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluar los individuos cuya fitness cambió
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Reemplazar la población antigua por la descendencia
        population[:] = offspring
        hall_of_fame.update(population)

        # Imprimir métricas de la generación actual
        fits = [ind.fitness.values[0] for ind in population]
        print(f"Generación {gen:2d} | Max Sharpe: {max(fits):.4f} | Avg Sharpe: {np.mean(fits):.4f}")

    best_strategy = hall_of_fame[0]
    print("\n--- ¡Evolución Finalizada! ---")
    print(f"Mejor Árbol Encontrado: {best_strategy}")
    print(f"Fitness (Sharpe Ajustado): {best_strategy.fitness.values[0]:.4f}")

    return best_strategy