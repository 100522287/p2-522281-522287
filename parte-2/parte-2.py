#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parte 2: Resolución del problema del camino más corto mediante A*.

Este script encuentra el camino más corto entre dos vértices de un grafo
de la 9th DIMACS Shortest-Path Challenge, utilizando el algoritmo A* con
la distancia geodésica (Haversine) como heurística admisible.

Uso: ./parte-2.py <vertice-1> <vertice-2> <nombre-del-mapa> <fichero-salida>

Ejemplo:
    ./parte-2.py 1 309 USA-road-d.BAY solucion

El algoritmo A* garantiza encontrar la solución óptima cuando:
- La heurística h(n) es admisible (no sobreestima el coste real)
- La heurística h(n) es consistente (satisface desigualdad triangular)

La distancia geodésica cumple ambas propiedades porque representa
el camino más corto posible sobre la superficie terrestre.
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
    
    # Resolver con A*
    algoritmo = AlgoritmoAStarConPadres(grafo, vertice_1, vertice_2)
    
    tiempo_inicio = time.time()
    camino, coste = algoritmo.resolver()
    tiempo_fin = time.time()
    
    tiempo_ejecucion = tiempo_fin - tiempo_inicio
    expansiones = algoritmo.expansiones
    
    # Calcular nodos por segundo
    if tiempo_ejecucion > 0:
        nodos_por_segundo = expansiones / tiempo_ejecucion
    else:
        nodos_por_segundo = 0
    
    # Mostrar resultados
    if camino is not None:
        print(f"Solución óptima encontrada con coste {coste}")
    else:
        print("No se encontró solución")
    
    print()
    print(f"Tiempo de ejecución: {tiempo_ejecucion:.2f} segundos")
    print(f"# expansiones      : {expansiones} ({nodos_por_segundo:.2f} nodes/sec)")
    
    # Escribir solución en fichero
    with open(fichero_salida, 'w') as f:
        if camino is not None:
            f.write(formatear_camino(camino))
            f.write('\n')
        else:
            f.write("No se encontró solución\n")


if __name__ == '__main__':
    main()