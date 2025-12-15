"""
Parte 1: Resolución del problema BINAIRO mediante Satisfacción de Restricciones.
El problema consiste en rellenar una rejilla n×n con
discos blancos (O) y negros (X) cumpliendo las siguientes restricciones:
  - No debe quedar ninguna posición vacía.
  - El número de discos blancos y negros en cada fila y columna debe ser igual.
  - No es posible disponer más de dos discos del mismo color consecutivamente.

Uso: python3 parte-1.py <fichero-entrada> <fichero-salida>
"""

import sys 
from constraint import Problem, ExactSumConstraint


def leer_instancia(fichero_entrada):
    """
    Lee el fichero de entrada y devuelve la matriz del problema.
    
    Argumentos:
        fichero_entrada: Ruta al fichero con la instancia del problema.
        
    Returns:
        Lista de listas representando la rejilla del problema.
        '.' indica celda vacía, 'X' disco negro, 'O' disco blanco.
    """
    with open(fichero_entrada, 'r') as f:
        lineas = f.read().strip().split('\n') # Leer todas las líneas del archivo
    
    matriz = []
    for linea in lineas:
        fila = list(linea.strip()) 
        matriz.append(fila) # Añadir cada fila a la matriz

    return matriz # Devolver la matriz completa


def formato_rejilla(matriz, n):
    """
    Genera la representación visual de la rejilla.
    
    Argumentos:
        matriz: Lista de listas con los valores de las celdas.
        n: Dimensión de la rejilla.
        
    Returns:
        String con la representación formateada de la rejilla.
    """
    separador = '+---' * n + '+'
    lineas = [separador]
    
    for fila in matriz:
        contenido = '|'
        for celda in fila:
            if celda == '.':
                contenido += '   |' # Celda vacía
            elif celda == 'X':
                contenido += ' X |' # Disco negro
            elif celda == 'O':
                contenido += ' O |' # Disco blanco
            # estos casos son para después de resolver
            elif celda == 1:
                contenido += ' X |' # Disco negro
            elif celda == 0:
                contenido += ' O |' # Disco blanco
            else:
                contenido += ' ' + str(celda) + ' |'
        lineas.append(contenido)
        lineas.append(separador)
    
    return '\n'.join(lineas) # Devolver la rejilla formateada como string


def restriccion_no_tres_consecutivos(v1, v2, v3):
    """
    Verifica que tres valores consecutivos no sean todos iguales (todos blancos o todos negros).
    
    Esta restricción asegura que no haya más de dos discos del mismo
    color consecutivos en una fila o columna.
    
    Argumentos:
        v1, v2, v3: Valores de tres celdas consecutivas.
        
    Returns:
        True si la restricción se satisface, False en caso contrario.
    """
    # No pueden ser los tres iguales (ni todos 0, ni todos 1)
    suma = v1 + v2 + v3
    return suma >= 1 and suma <= 2


def crear_modelo(matriz):
    """
    Crea el modelo de satisfacción de restricciones para BINAIRO.
    
    El modelo sigue la formalización:
    - Variables: x_ij para cada celda (i,j)
    - Dominios: {0,1} para celdas vacías, valor fijo para celdas pre-asignadas
    - Restricciones: 
            C1 (equilibrio filas), 
            C2 (equilibrio columnas),
            C3 (no tres consecutivos en filas),
            C4 (no tres consecutivos en columnas)
    
    Argumentos:
        matriz: Rejilla del problema con valores iniciales.
        
    Returns:
        Objeto Problem configurado con el modelo CSP.
    """
    n = len(matriz)
    problem = Problem()
    
    # Creación de variables con sus dominios
    # Cada variable se identifica como (i, j) representando la celda en fila i, columna j
    for i in range(n):
        for j in range(n):
            celda = matriz[i][j]
            if celda == '.':
                # Celda vacía: dominio {0, 1} donde 0=blanco, 1=negro
                problem.addVariable((i, j), [0, 1])
            elif celda == 'X':
                # Disco negro pre-asignado
                problem.addVariable((i, j), [1])
            elif celda == 'O':
                # Disco blanco pre-asignado
                problem.addVariable((i, j), [0])
    
    # C1: Equilibrio en cada fila
    # La suma de valores en cada fila debe ser exactamente n/2
    for i in range(n):
        variables_fila = [(i, j) for j in range(n)]
        problem.addConstraint(ExactSumConstraint(n // 2), variables_fila)
    
    # C2: Equilibrio en cada columna
    # La suma de valores en cada columna debe ser exactamente n/2
    for j in range(n):
        variables_columna = [(i, j) for i in range(n)]
        problem.addConstraint(ExactSumConstraint(n // 2), variables_columna)
    
    # C3: No más de dos consecutivos en filas
    # Para cada triplete horizontal, no pueden ser todos iguales
    for i in range(n):
        for j in range(n - 2):
            variables_triplete = [(i, j), (i, j + 1), (i, j + 2)]
            problem.addConstraint(restriccion_no_tres_consecutivos, variables_triplete)
    
    # C4: No más de dos consecutivos en columnas
    # Para cada triplete vertical, no pueden ser todos iguales
    for j in range(n):
        for i in range(n - 2):
            variables_triplete = [(i, j), (i + 1, j), (i + 2, j)]
            problem.addConstraint(restriccion_no_tres_consecutivos, variables_triplete)
    
    return problem


def solucion_a_matriz(dic, n):
    """
    Convierte el diccionario de solución a formato matriz.
    
    Argumentos:
        dic: Diccionario con asignaciones {(i,j): valor}.
        n: Dimensión de la rejilla.
        
    Returns:
        Lista de listas con los valores de la solución.
    """
    matriz = [[0 for _ in range(n)] for _ in range(n)] # Inicializar matriz llena de ceros
    for (i, j), valor in dic.items():
        matriz[i][j] = valor
    return matriz


def main():
    """
    Función principal que ejecuta el solver de BINAIRO.
    """
    # Verificación de argumentos
    if len(sys.argv) != 3:
        print("Uso: python3 parte-1.py <fichero-entrada> <fichero-salida>")
        sys.exit(1)
    
    fichero_entrada = sys.argv[1]
    fichero_salida = sys.argv[2]
    
    # Lectura de la instancia
    matriz = leer_instancia(fichero_entrada)
    n = len(matriz)
    
    # Mostrar instancia en pantalla
    print(formato_rejilla(matriz, n))
    
    # Crear y resolver el modelo CSP
    problem = crear_modelo(matriz)
    
    # Obtener todas las soluciones
    soluciones = problem.getSolutions()
    num_soluciones = len(soluciones)
    
    # Mostrar número de soluciones
    if num_soluciones == 1:
        print("Una solución encontrada")
    else:
        print(f"{num_soluciones} soluciones encontradas")
    
    # Escribir en fichero de salida
    with open(fichero_salida, 'w') as f:
        # Primero escribir la instancia original
        f.write(formato_rejilla(matriz, n))
        f.write('\n\n')
        
        # Luego escribir una solución (si existe)
        if num_soluciones > 0:
            solucion = soluciones[0]
            matriz_solucion = solucion_a_matriz(solucion, n)
            f.write(formato_rejilla(matriz_solucion, n))
            f.write('\n')


if __name__ == '__main__':
    main()