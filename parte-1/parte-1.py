
import sys 
from constraint import Problem, ExactSumConstraint


# En este fichero se implementa la solucion a la primera parte de la practica


# Funcion que lee el fichero de entrada y devuelve la matriz del problema.
def leer_instancia(fichero_entrada):

    # Abre el fichero en modo lectura de forma segura (se cierra solo al acabar)
    with open(fichero_entrada, 'r') as f:
        lineas = f.read().strip().split('\n') # Lee todas las líneas del archivo
    
    matriz = [] # Inicializa una lista donde se guardará el tablero procesado
    # bucle que recorre todas las lineas
    for linea in lineas:
        # Convierte la fila en una lista de caracteres
        fila = list(linea.strip()) 
        matriz.append(fila) # Añade cada fila a la matriz

    return matriz # Devuelve la matriz completa



# Funcion que genera la representación visual de la rejilla.
def formato_rejilla(matriz, n):

    separador = '+---' * n + '+' # Crea la linea horizontal divisoria
    # Inicializa la lista de lineas a imprimir empezando con el borde superior
    lineas = [separador]
    
    # bucle que se repite para cada fila en la matriz para pintar el rectangulo
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



# Verifica que tres valores consecutivos no sean todos iguales (todos blancos o todos negros).
# Esta restricción asegura que no haya más de dos discos del mismo color consecutivos en una fila o columna.
def restriccion_no_tres_consecutivos(v1, v2, v3):
    suma = v1 + v2 + v3 # No pueden ser los tres iguales (ni todos 0, ni todos 1)
    return suma >= 1 and suma <= 2


# Funcion que crea el modelo de satisfacción de restricciones para BINAIRO.
def crear_modelo(matriz):
    """
    El modelo sigue la siguiente formalización:
    - Variables: x_ij para cada celda (i,j)
    - Dominios: {0,1} para celdas vacías, valor fijo para celdas pre-asignadas
    - Restricciones: 
            C1 (equilibrio filas), 
            C2 (equilibrio columnas),
            C3 (no tres consecutivos en filas),
            C4 (no tres consecutivos en columnas)
    """
    n = len(matriz) # Obtiene el tamaño de la rejilla 
    problem = Problem() # Crea una instancia vacia del solucionador
    
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


# Solucion que convierte el diccionario de solucion a formato matriz
def solucion_a_matriz(dic, n):
    matriz = [[0 for _ in range(n)] for _ in range(n)] # Inicializa una matriz llena de ceros
    # Itera sobre la matriz rellenando las posiciones con ceros o unos como corresponda
    for (i, j), valor in dic.items():
        matriz[i][j] = valor
    return matriz



# Función principal que ejecuta el solver de BINAIRO.
def main():
    # Verificación de argumentos
    if len(sys.argv) != 3:
        print("Uso: python3 parte-1.py <fichero-entrada.in <fichero-salida.out>")
        sys.exit(1)
    
    # Recibe los archivos de entrada y salida
    fichero_entrada = sys.argv[1]
    fichero_salida = sys.argv[2]
    
    # Se llama a la funcion auxiliar leer_instancia para obtener el "tablero"
    matriz = leer_instancia(fichero_entrada)
    n = len(matriz) # Calcula las dimensiones del tablero
    
    # Muestra la instancia en pantalla
    print(formato_rejilla(matriz, n))
    
    # Creaa y resuelve el modelo CSP
    problem = crear_modelo(matriz)
    
    # Obtiene todas las soluciones
    soluciones = problem.getSolutions()
    num_soluciones = len(soluciones)
    
    # Muestra número de soluciones
    if num_soluciones == 1:
        print("Una solución encontrada")
    else:
        print(f"{num_soluciones} soluciones encontradas")
    
    # Escribe en el fichero de salida
    with open(fichero_salida, 'w') as f:
        # Primero escribir la instancia original
        f.write(formato_rejilla(matriz, n))
        f.write('\n\n')
        
        # Luego, escribie una solución (si existe)
        if num_soluciones > 0:
            solucion = soluciones[0]
            matriz_solucion = solucion_a_matriz(solucion, n)
            f.write(formato_rejilla(matriz_solucion, n))
            f.write('\n')


if __name__ == '__main__':
    main()