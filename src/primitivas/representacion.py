import operator
import random
import functools
# 1. Función de división protegida para evitar errores matemáticos
DANGER_EPSILON = 1e-6
def protected_div(left, right):
    if abs(right) < DANGER_EPSILON:
        return 1.0
    return left / right

def setup_gp_pset():
    """Define el conjunto primitivo (Terminales y Funciones) para el TFG."""
    # Creamos un conjunto de primitivas tipado o genérico (aquí genérico con tipos float/bool)
    pset = gp.PrimitiveSet("MAIN", arity=5)
    
    # Renombramos las variables de entrada para que coincidan con tus columnas del Parquet
    pset.renameArguments(ARG0="Price_to_SMA20")
    pset.renameArguments(ARG1="VIX_Close")
    pset.renameArguments(ARG2="IV_ATM_Call")
    pset.renameArguments(ARG3="IV_Skew_Put_Call")
    pset.renameArguments(ARG4="VRP")

    # Añadir Funciones matemáticas y lógicas (Conjunto F)
    pset.addPrimitive(operator.add, 2, name="add")
    pset.addPrimitive(operator.sub, 2, name="sub")
    pset.addPrimitive(operator.mul, 2, name="mul")
    pset.addPrimitive(protected_div, 2, name="div")
    
    # Funciones condicionales para la toma de decisiones de trading
    pset.addPrimitive(lambda x, y: 1.0 if x > y else 0.0, 2, name="gt")
    pset.addPrimitive(lambda cond, out1, out2: out1 if cond > 0.5 else out2, 3, name="if_then_else")

    # Constantes efímeras (números aleatorios generados por el algoritmo)
  # Constantes efímeras (números aleatorios generados por el algoritmo)
    # Constantes efímeras (números aleatorios generados por el algoritmo)
    set.addEphemeralConstant("rand100", functools.partial(random.uniform, -2.0, 2.0))
    return pset