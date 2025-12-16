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
    
    print("--- Ejecutando A* (Búsqueda Informada) ---")
    algoritmo_astar = AlgoritmoAStarConPadres(grafo, vertice_1, vertice_2)
        
    tiempo_inicio = time.time()
    camino_astar, coste_astar = algoritmo_astar.resolver()
    tiempo_fin = time.time()
    
    tiempo_astar = tiempo_fin - tiempo_inicio
    expansiones_astar = algoritmo_astar.expansiones
    
    print(f"Coste: {coste_astar}")
    print(f"Expansiones: {expansiones_astar}")
    print(f"Tiempo: {tiempo_astar:.4f} s\n")

    print("--- Ejecutando Dijkstra (Fuerza Bruta) ---")
    algoritmo_dijkstra = AlgoritmoDijkstra(grafo, vertice_1, vertice_2)
    
    tiempo_inicio = time.time()
    _, coste_dijkstra = algoritmo_dijkstra.resolver() # Solo interesa el coste, el camino lo almacena pero no se usa aquí
    tiempo_fin = time.time()
    
    tiempo_dijkstra = tiempo_fin - tiempo_inicio
    expansiones_dijkstra = algoritmo_dijkstra.expansiones

    print(f"Coste: {coste_dijkstra}")
    print(f"Expansiones: {expansiones_dijkstra}")
    print(f"Tiempo: {tiempo_dijkstra:.4f} s\n")

    # Comparativa
    if expansiones_dijkstra > 0:
        ahorro = 100 * (1 - expansiones_astar / expansiones_dijkstra)
        print(f"A* expandió un {ahorro:.2f}% menos de nodos que Dijkstra.")
    
    # Escribir solución en fichero
    with open(fichero_salida, 'w') as f:
        if camino_astar is not None:
            f.write(formatear_camino(camino_astar))
            f.write('\n')
        else:
            f.write("No se encontró solución\n")


if __name__ == '__main__':
    main()