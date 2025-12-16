#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suite de pruebas automatizadas para la práctica de Búsqueda Heurística.
Compara A* contra Dijkstra y verifica casos borde.
"""

import sys
import os
import random
import time
from grafo import Grafo
from algoritmo import AlgoritmoAStarConPadres, AlgoritmoDijkstra

# Configuración de pruebas
NUM_PRUEBAS_ALEATORIAS = 20  # Número de rutas aleatorias a probar por mapa
MAPAS_A_PROBAR = ["USA-road-d.NY", "USA-road-d.BAY"]

def test_caso_base(grafo, nombre_mapa):
    """Prueba 1: Origen == Destino (Debe dar coste 0)"""
    print(f"\n[TEST] Caso Base (Origen = Destino) en {nombre_mapa}")
    
    nodos = list(grafo.coordenadas.keys())
    nodo = random.choice(nodos)
    
    astar = AlgoritmoAStarConPadres(grafo, nodo, nodo)
    camino, coste = astar.resolver()
    
    if coste == 0 and camino and len(camino) == 1:
        print(f"✅ PASSED: Coste 0 correctamente detectado para nodo {nodo}.")
    else:
        print(f"❌ FAILED: Se esperaba coste 0, se obtuvo {coste}.")

def test_comparativa_aleatoria(grafo, nombre_mapa):
    """Prueba 2: Comparativa A* vs Dijkstra en rutas aleatorias"""
    print(f"\n[TEST] Ejecutando {NUM_PRUEBAS_ALEATORIAS} comparativas A* vs Dijkstra en {nombre_mapa}...")
    
    nodos = list(grafo.coordenadas.keys())
    aciertos = 0
    ahorros = []
    
    for i in range(NUM_PRUEBAS_ALEATORIAS):
        origen = random.choice(nodos)
        destino = random.choice(nodos)
        
        # Evitar caso trivial
        while origen == destino:
            destino = random.choice(nodos)
            
        # 1. Ejecutar Dijkstra (La verdad absoluta)
        dijkstra = AlgoritmoDijkstra(grafo, origen, destino)
        camino_d, coste_d = dijkstra.resolver()
        
        # 2. Ejecutar A* (La heurística)
        astar = AlgoritmoAStarConPadres(grafo, origen, destino)
        camino_a, coste_a = astar.resolver()
        
        # 3. Verificaciones
        # Caso A: Ambos no encuentran camino
        if camino_d is None and camino_a is None:
            print(f"  Iteración {i+1}: Ambos algoritmos determinaron que es inalcanzable. (OK)")
            aciertos += 1
            continue
            
        # Caso B: Uno encuentra y el otro no (Error grave)
        if (camino_d is None) != (camino_a is None):
            print(f"❌ FAILED Iter {i+1}: Inconsistencia de alcanzabilidad. Dijkstra: {camino_d is not None}, A*: {camino_a is not None}")
            continue
            
        # Caso C: Ambos encuentran camino -> Verificar optimalidad
        # Usamos un pequeño margen de error por flotantes si fuera necesario, 
        # pero aquí son enteros o sumas directas, debería ser exacto.
        if abs(coste_d - coste_a) < 1e-6:
            # Calcular ahorro de expansiones
            if dijkstra.expansiones > 0:
                ahorro = 100 * (1 - astar.expansiones / dijkstra.expansiones)
                ahorros.append(ahorro)
            aciertos += 1
            # Opcional: imprimir puntos cada 5 tests
            if (i+1) % 5 == 0:
                 print(f"  Iteración {i+1}: Costes coinciden ({coste_a}). Ahorro exp: {ahorro:.1f}%")
        else:
            print(f"❌ FAILED Iter {i+1}: Costes difieren. Dijkstra={coste_d}, A*={coste_a}. A* no es admisible o hay error.")

    print(f"Resultados {nombre_mapa}: {aciertos}/{NUM_PRUEBAS_ALEATORIAS} pruebas exitosas.")
    if ahorros:
        print(f"Ahorro medio de expansiones: {sum(ahorros)/len(ahorros):.2f}%")

def test_vertices_invalidos(grafo):
    """Prueba 3: Manejo de vértices inexistentes"""
    print("\n[TEST] Prueba de vértices inválidos")
    vertice_fake = -9999
    
    try:
        # Intentamos instanciar o resolver con un nodo que no existe
        # Nota: Tu implementación actual de heurística fallará con KeyError al buscar coordenadas
        # Esto valida que el programa principal debe chequear existencia antes.
        astar = AlgoritmoAStarConPadres(grafo, vertice_fake, list(grafo.coordenadas.keys())[0])
        astar.heuristica(vertice_fake)
        print("⚠️ WARNING: El código aceptó un vértice inválido sin error (debería fallar o controlarse).")
    except KeyError:
        print("✅ PASSED: El sistema detectó correctamente el acceso a coordenadas de vértice inexistente.")
    except Exception as e:
        print(f"ℹ️ INFO: Saltó otra excepción controlada: {e}")

def main():
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    
    for mapa in MAPAS_A_PROBAR:
        ruta_mapa = os.path.join(directorio_script, mapa)
        # Comprobar si existen los ficheros .gr y .co
        if not os.path.exists(ruta_mapa + ".gr"):
            print(f"\nSaltando mapa {mapa} (no se encontraron los archivos .gr/.co)")
            continue
            
        print(f"\n{'='*60}")
        print(f"CARGANDO MAPA: {mapa}")
        print(f"{'='*60}")
        
        grafo = Grafo()
        inicio = time.time()
        grafo.cargar(ruta_mapa)
        print(f"Grafo cargado en {time.time() - inicio:.2f}s. V: {grafo.num_vertices}, A: {grafo.num_arcos}")
        
        if grafo.num_vertices == 0:
            print("Error: El grafo está vacío.")
            continue

        # Ejecutar batería
        test_caso_base(grafo, mapa)
        test_comparativa_aleatoria(grafo, mapa)
        test_vertices_invalidos(grafo)

if __name__ == '__main__':
    main()