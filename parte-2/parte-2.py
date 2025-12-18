#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import os

from grafo import Grafo
from algoritmo import AlgoritmoAEstrella


# Aquí se ejecuta el codigo principal de la parte 2 del proyecto (la funcion principa es main)



# Funcion que formatea el camino para escribirlo en el fichero de salida
def formatear_camino(camino):
    # Si no hay camino, no se retorna nada
    if not camino:
        return "No hay camino"

    partes = [] # Lista donde se alamcenará cada parte del camino
    # Recorre cada paso del camino solución
    for i, (nodo, coste_arco) in enumerate(camino):
        # Si es el primer nodo se añade tal cual
        if i == 0:
            partes.append(str(nodo))
        # si no es el primer nodo:
        else:
            # Añade el coste del tramo entre parentesis
            partes.append(f"({coste_arco})")
            #Añade el id del nodo
            partes.append(str(nodo))
    
    # Retorna todos los elementos de partes unidos con guiones
    return " - ".join(partes)



# Función principal que ejecuta el solver de camino más corto
# Ejecuta tanto A* como Dijkstra para poder comparar el numero de expansiones y demostrar la eficiencia de la heuristica
def main():
    # Verificación de argumentos
    if len(sys.argv) != 5:
        print("Uso: ./parte-2.py <vertice-1> <vertice-2> <nombre-del-mapa> <fichero-salida>")
        sys.exit(1)
    
    # Parsea los argumentos pasados
    vertice_1 = int(sys.argv[1])
    vertice_2 = int(sys.argv[2])
    nombre_mapa = sys.argv[3]
    fichero_salida = sys.argv[4]
    
    # Se crea una instancia grafo
    grafo = Grafo()
    
    # Se determina la ruta base del mapa
    # Si no tiene directorio, se usa el directorio del script
    if os.path.dirname(nombre_mapa) == '':
        directorio_script = os.path.dirname(os.path.abspath(__file__))
        nombre_mapa_completo = os.path.join(directorio_script, nombre_mapa)
    else:
        nombre_mapa_completo = nombre_mapa
    
    # Se llama a la funcion cargar, que lee los archivos y carga el grafo 
    grafo.cargar(nombre_mapa_completo)
    
    # Muestra información del grafo
    print(f"# vertices: {grafo.num_vertices}")
    print(f"# arcos   : {grafo.num_arcos}")
    
    # Se verifica que los vértices existen
    if not grafo.existe_vertice(vertice_1):
        print(f"Error: el vértice {vertice_1} no existe en el grafo")
        sys.exit(1)
    
    if not grafo.existe_vertice(vertice_2):
        print(f"Error: el vértice {vertice_2} no existe en el grafo")
        sys.exit(1)
    

    # Se ejecuta A* 
    print("--- Ejecutando A* ---")
    # se crea una instancia de A*, pasnado como argumentos el grafo, el vertice origen y el vertice destino
    algoritmo_astar = AlgoritmoAEstrella(grafo, vertice_1, vertice_2)
    # Se mide cuanto tarda    
    tiempo_inicio = time.time()
    # Se llama a la funcion de resolver, que aplica el algoritmo A* y devuelve el coste y el camino optimo
    camino_astar, coste_astar = algoritmo_astar.resolver()
    tiempo_fin = time.time()
    # Se calcula el tiempo que ha tardado en ejecutarse el algoritmo
    tiempo_astar = tiempo_fin - tiempo_inicio
    # numero de nodos exapandidos por el algoritmo
    expansiones_astar = algoritmo_astar.expansiones
    
    # Se imprimen los datos obtenidos al ejecutar a* por pantalla
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

    
    # Determinar la ruta del fichero de salida
    if os.path.dirname(fichero_salida) == '':
        directorio_script = os.path.dirname(os.path.abspath(__file__))
        fichero_salida_completo = os.path.join(directorio_script, fichero_salida)
    else:
        fichero_salida_completo = fichero_salida
    # Una vez obtenida la ruta del fichero de salida, se escribe en él la solucion llamando a formatear_camino 
    with open(fichero_salida_completo, 'w') as f:
        if camino_astar is not None:
            f.write(formatear_camino(camino_astar))
            f.write('\n')
        else:
            f.write("No se encontró solución\n")


# Ejecuta el main
if __name__ == '__main__':
    main()
    