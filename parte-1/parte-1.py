#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parte 1: Resolución del problema BINAIRO mediante Satisfacción de Restricciones.

Este script resuelve instancias del puzzle BINAIRO utilizando la librería
python-constraint. El problema consiste en rellenar una rejilla n×n con
discos blancos (O) y negros (X) cumpliendo las siguientes restricciones:
  - No debe quedar ninguna posición vacía.
  - El número de discos blancos y negros en cada fila y columna debe ser igual.
  - No es posible disponer más de dos discos del mismo color consecutivamente.

Uso: ./parte-1.py <fichero-entrada> <fichero-salida>
"""

import sys
from constraint import Problem, ExactSumConstraint


def leer_instancia(fichero_entrada):
    """
    Lee el fichero de entrada y devuelve la matriz del problema.
    
    Args:
        fichero_entrada: Ruta al fichero con la instancia del problema.
        
    Returns:
        Lista de listas representando la rejilla del problema.
        '.' indica celda vacía, 'X' disco negro, 'O' disco blanco.
    """
    with open(fichero_entrada, 'r') as f:
        lineas = f.read().strip().split('\n')
    
    matriz = []
    for linea in lineas:
        fila = list(linea.strip())
        matriz.append(fila)
    
    return matriz


def formato_rejilla(matriz, n):
    """
    Genera la representación visual de la rejilla.
    
    Args:
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
                contenido += '   |'
            elif celda == 'X':
                contenido += ' X |'
            elif celda == 'O':
                contenido += ' O |'
            elif celda == 1:
                contenido += ' X |'
            elif celda == 0:
                contenido += ' O |'
            else:
                contenido += ' ' + str(celda) + ' |'
        lineas.append(contenido)
        lineas.append(separador)
    
    return '\n'.join(lineas)


def restriccion_no_tres_consecutivos(v1, v2, v3):
    """
    Verifica que tres valores consecutivos no sean todos iguales.
    
    Esta restricción asegura que no haya más de dos discos del mismo
    color consecutivos en una fila o columna.
    
    Args:
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
    - Restricciones: C1 (equilibrio filas), C2 (equilibrio columnas),
                     C3 (no tres consecutivos en filas), C4 (no tres consecutivos en columnas)
    
    Args:
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
    
    # Restricción C1: Equilibrio en cada fila
    # La suma de valores en cada fila debe ser exactamente n/2
    for i in range(n):
        variables_fila = [(i, j) for j in range(n)]
        problem.addConstraint(ExactSumConstraint(n // 2), variables_fila)
    
    # Restricción C2: Equilibrio en cada columna
    # La suma de valores en cada columna debe ser exactamente n/2
    for j in range(n):
        variables_columna = [(i, j) for i in range(n)]
        problem.addConstraint(ExactSumConstraint(n // 2), variables_columna)
    
    # Restricción C3: No más de dos consecutivos en filas
    # Para cada triplete horizontal, no pueden ser todos iguales
    for i in range(n):
        for j in range(n - 2):
            variables_triplete = [(i, j), (i, j + 1), (i, j + 2)]
            problem.addConstraint(restriccion_no_tres_consecutivos, variables_triplete)
    
    # Restricción C4: No más de dos consecutivos en columnas
    # Para cada triplete vertical, no pueden ser todos iguales
    for j in range(n):
        for i in range(n - 2):
            variables_triplete = [(i, j), (i + 1, j), (i + 2, j)]
            problem.addConstraint(restriccion_no_tres_consecutivos, variables_triplete)
    
    return problem


def solucion_a_matriz(solucion, n):
    """
    Convierte el diccionario de solución a formato matriz.
    
    Args:
        solucion: Diccionario con asignaciones {(i,j): valor}.
        n: Dimensión de la rejilla.
        
    Returns:
        Lista de listas con los valores de la solución.
    """
    matriz = [[0 for _ in range(n)] for _ in range(n)]
    for (i, j), valor in solucion.items():
        matriz[i][j] = valor
    return matriz


def main():
    """
    Función principal que ejecuta el solver de BINAIRO.
    """
    # Verificación de argumentos
    if len(sys.argv) != 3:
        print("Uso: ./parte-1.py <fichero-entrada> <fichero-salida>")
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
        print(f"{num_soluciones} solución encontrada")
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