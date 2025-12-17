#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parte 2: Resolución del problema del camino más corto mediante A* con Dial's Bucket.

Este script encuentra el camino más corto entre dos vértices de un grafo
de la 9th DIMACS Shortest-Path Challenge, utilizando el algoritmo A* con
la distancia geodésica (Haversine) como heurística admisible.

IMPORTANTE: Esta implementación utiliza Dial's Bucket en lugar de heap binario
para la cola de prioridad, lo cual es más eficiente para grafos con pesos
enteros como los de DIMACS.

Uso: ./parte-2.py <vertice-1> <vertice-2> <nombre-del-mapa> <fichero-salida>

Ejemplo:
    ./parte-2.py 1 309 USA-road-d.BAY solucion

El algoritmo A* garantiza encontrar la solución óptima cuando:
- La heurística h(n) es admisible (no sobreestima el coste real)
- La heurística h(n) es consistente (satisface desigualdad triangular)

La distancia geodésica cumple ambas propiedades porque representa
el camino más corto posible sobre la superficie terrestre.

Dial's Bucket:
- Estructura de datos que usa un array de "buckets" indexados por coste
- Inserción: O(1)
- Extracción del mínimo: O(C) amortizado, donde C es el rango de costes
- Más eficiente que heap para grafos con pesos enteros acotados
"""

import sys
import time
import os

from grafo import Grafo
from algoritmo import AlgoritmoAStarConPadres, AlgoritmoDijkstra


def formatear_camino(camino):
    """
    Formatea el camino para escribirlo en el fichero de salida.
    
    Formato: <inicio> - (coste) - <vertice> - (coste) - ... - <final>
    
    Args:
        camino: Lista de tuplas (nodo, coste_arco).
        
    Returns:
        String con el camino formateado.
    """
    if not camino:
        return "No hay camino"
    
    partes = []
    for i, (nodo, coste_arco) in enumerate(camino):
        if i == 0:
            partes.append(str(nodo))
        else:
            partes.append(f"({coste_arco})")
            partes.append(str(nodo))
    
    return " - ".join(partes)


def main():
    """
    Función principal que ejecuta el solver de camino más corto.
    
    Ejecuta tanto A* (con heurística) como Dijkstra (fuerza bruta)
    para poder comparar el número de expansiones y demostrar la
    eficiencia de la heurística.
    """
    # Verificación de argumentos
    if len(sys.argv) != 5:
        print("Uso: ./parte-2.py <vertice-1> <vertice-2> <nombre-del-mapa> <fichero-salida>")
        sys.exit(1)
    
    vertice_1 = int(sys.argv[1])
    vertice_2 = int(sys.argv[2])
    nombre_mapa = sys.argv[3]
    fichero_salida = sys.argv[4]
    
    # Cargar el grafo
    grafo = Grafo()
    
    # Determinar la ruta base del mapa
    # Si no tiene directorio, usar el directorio del script
    if os.path.dirname(nombre_mapa) == '':
        directorio_script = os.path.dirname(os.path.abspath(__file__))
        nombre_mapa_completo = os.path.join(directorio_script, nombre_mapa)
    else:
        nombre_mapa_completo = nombre_mapa
    
    # Cargar grafo y coordenadas
    grafo.cargar(nombre_mapa_completo)
    
    # Mostrar información del grafo
    print(f"# vertices: {grafo.num_vertices}")
    print(f"# arcos   : {grafo.num_arcos}")
    
    # Verificar que los vértices existen
    if not grafo.existe_vertice(vertice_1):
        print(f"Error: el vértice {vertice_1} no existe en el grafo")
        sys.exit(1)
    
    if not grafo.existe_vertice(vertice_2):
        print(f"Error: el vértice {vertice_2} no existe en el grafo")
        sys.exit(1)
    
    # Ejecutar A* (búsqueda informada con Dial's Bucket)
    print("--- Ejecutando A* con Dial's Bucket (Búsqueda Informada) ---")
    algoritmo_astar = AlgoritmoAStarConPadres(grafo, vertice_1, vertice_2)
        
    tiempo_inicio = time.time()
    camino_astar, coste_astar = algoritmo_astar.resolver()
    tiempo_fin = time.time()
    
    tiempo_astar = tiempo_fin - tiempo_inicio
    expansiones_astar = algoritmo_astar.expansiones
    
    if coste_astar is not None:
        print(f"Solución óptima encontrada con coste {coste_astar}")
    else:
        print("No se encontró solución")
    print(f"Tiempo de ejecución: {tiempo_astar:.2f} segundos")
    if tiempo_astar > 0:
        print(f"# expansiones   : {expansiones_astar} ({expansiones_astar/tiempo_astar:.2f} nodes/sec)")
    else:
        print(f"# expansiones   : {expansiones_astar}")
    print()

    # Ejecutar Dijkstra (fuerza bruta con Dial's Bucket)
    print("--- Ejecutando Dijkstra con Dial's Bucket (Fuerza Bruta) ---")
    algoritmo_dijkstra = AlgoritmoDijkstra(grafo, vertice_1, vertice_2)
    
    tiempo_inicio = time.time()
    _, coste_dijkstra = algoritmo_dijkstra.resolver()
    tiempo_fin = time.time()
    
    tiempo_dijkstra = tiempo_fin - tiempo_inicio
    expansiones_dijkstra = algoritmo_dijkstra.expansiones

    if coste_dijkstra is not None:
        print(f"Solución óptima encontrada con coste {coste_dijkstra}")
    else:
        print("No se encontró solución")
    print(f"Tiempo de ejecución: {tiempo_dijkstra:.2f} segundos")
    if tiempo_dijkstra > 0:
        print(f"# expansiones   : {expansiones_dijkstra} ({expansiones_dijkstra/tiempo_dijkstra:.2f} nodes/sec)")
    else:
        print(f"# expansiones   : {expansiones_dijkstra}")
    print()

    # Comparativa
    print("--- Comparativa ---")
    if expansiones_dijkstra > 0 and expansiones_astar is not None:
        ahorro = 100 * (1 - expansiones_astar / expansiones_dijkstra)
        print(f"A* expandió un {ahorro:.2f}% menos de nodos que Dijkstra.")
    
    if coste_astar == coste_dijkstra:
        print("Ambos algoritmos encontraron la misma solución óptima.")
    
    # Escribir solución en fichero
    # Determinar la ruta del fichero de salida
    if os.path.dirname(fichero_salida) == '':
        directorio_script = os.path.dirname(os.path.abspath(__file__))
        fichero_salida_completo = os.path.join(directorio_script, fichero_salida)
    else:
        fichero_salida_completo = fichero_salida
    
    with open(fichero_salida_completo, 'w') as f:
        if camino_astar is not None:
            f.write(formatear_camino(camino_astar))
            f.write('\n')
        else:
            f.write("No se encontró solución\n")


if __name__ == '__main__':
    main()