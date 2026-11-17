import numpy as np
import pandas as pd
from deap import gp

def evaluar_estrategia_trading(individual, pset, df_master):
    """
    Función de Fitness: Compila el árbol sintáctico, lo ejecuta día a día 
    sobre el dataset maestro y calcula el Ratio de Sharpe de la estrategia.
    """
    # 1. Compilar el individuo (árbol de DEAP) a una función ejecutable en Python
    try:
        func = gp.compile(individual, pset)
    except Exception:
        return -999.0,  # Penalización si el árbol es sintácticamente inválido

    # 2. Extraer las variables del DataFrame que actúan como terminales
    p2sma = df_master["Price_to_SMA20"].values
    vix = df_master["VIX_Close"].values
    iv_atm = df_master["IV_ATM_Call"].values
    skew = df_master["IV_Skew_Put_Call"].values
    vrp = df_master["VRP"].values
    spx_returns = df_master["SPX_Return"].values

    # 3. Simular la estrategia día a día (Vectorizado o mediante bucle rápido)
    signals = np.zeros(len(df_master))
    for i in range(len(df_master)):
        try:
            # Evaluar el árbol con las variables del día i
            val = func(p2sma[i], vix[i], iv_atm[i], skew[i], vrp[i])
            # Si el resultado es > 0.5, adoptamos posición alcista (Long), si no, plano (Cash)
            signals[i] = 1.0 if val > 0.5 else 0.0
        except Exception:
            signals[i] = 0.0  # Si hay división por cero u error en tiempo de ejecución

    # 4. Calcular los retornos de la estrategia (Señal del día anterior por el retorno del SPX)
    strategy_returns = np.roll(signals, 1) * spx_returns
    strategy_returns[0] = 0.0  # El primer día sin operar

    # 5. Calcular la función de Fitness: Ratio de Sharpe anualizado con control de riesgo
    excess_returns = strategy_returns  # Asumiendo tasa libre de riesgo ~ 0 para simplificar
    if np.std(excess_returns) == 0:
        sharpe_ratio = 0.0
    else:
        sharpe_ratio = np.sqrt(252) * (np.mean(excess_returns) / np.std(excess_returns))

    # Opcional: Penalizar árboles demasiado largos (Bloat control) para cumplir requisitos de ingeniería
    penalty = 0.005 * len(individual)
    fitness_score = sharpe_ratio - penalty

    return fitness_score,