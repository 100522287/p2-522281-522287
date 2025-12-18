#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math


# Esta clase modela un grafo dirigido y ponderado donde los nodos tienen coordenadas geográficas (latitud/longitud).
class Grafo:
    
    # Radio de la Tierra en metros para el cálculo de distancias geodésicas
    RADIO_TIERRA = 6371000
    
    def __init__(self):
        self.num_vertices = 0 # Número de vértices en el grafo (inicialmente son 0)
        self.num_arcos = 0 # Número de arcos en el grafo (inicialmente son 0)
        # Diccionario que funcionara como lista de adyacencia 
        self.adyacencia = {} # Clave: id del nodo origen, valor: lista de tuplas (destino,coste)
        # Diccionario para guardar la ubicacion fisica de los nodos
        self.coordenadas = {} # Clave: id del nodo origen, valor: lista de tuplas (latitud, longitud)
    

    # carga la estructura del grafo desde un fichero .gr de DIMACS (que recibe como argumento)
    def cargar_grafo(self, fichero_gr):
        # Abre el archivo pasado como argumento en forma de solo lectura (se le pone un alias f)
        with open(fichero_gr, 'r') as f:
            # bucle que se repite para cada linea del fichero
            for linea in f:
                # Se limpian los espacios y se divide la linea en palabras
                partes = linea.strip().split()
                # Comprueba que el numero de palabras de la linea sea mayor que cuatro y que empieze por a, si no es así, se ignora
                # esto es así porque DIMACS usa lineas que empiezan por 'a' para definir las conexiones
                if len(partes) >= 4 and partes[0] == 'a':
                    # Se parsean las palabras leidas de la linea
                    origen = int(partes[1])
                    destino = int(partes[2])
                    coste = int(partes[3])
                    
                    # Se inicializa la lista de adyacencia si no existe
                    if origen not in self.adyacencia:
                        self.adyacencia[origen] = []
                    
                    # Se añade la nueva concexion a la lista de adyacencia
                    self.adyacencia[origen].append((destino, coste))
                    self.num_arcos += 1
    

    # Carga las coordenadas geográficas desde un fichero .co de DIMACS (pasado como argumento)
    def cargar_coordenadas(self, fichero_co):
        # Abre el archivo pasado como argumento en forma de solo lectura (se le pone un alias f)
        with open(fichero_co, 'r') as f:
            # Se limpian los espacios y se divide la linea en palabras
            for linea in f:
                # Comprueba que el numero de palabras de la linea sea mayor que cuatro y que empieze por w
                partes = linea.strip().split()
                if len(partes) >= 4 and partes[0] == 'v':
                    # Se parsean las palabras leidas de la linea
                    vertice = int(partes[1])
                    # Las coordenadas vienen multiplicadas por 1e6, por lo tanto, se dividen por ese numero
                    longitud = int(partes[2]) / 1e6
                    latitud = int(partes[3]) / 1e6
                    
                    # Se guarda la posicion del vertice en la lista de coordenadas
                    self.coordenadas[vertice] = (latitud, longitud)
                    self.num_vertices += 1
    

    # Funcion que carga el grafo completo llamando a las dos funciones anteriores
    # Se pasa como argumento el nombre base del grafo, sin las extensiones (que se añaden luego según corresponda)
    def cargar(self, nombre_base):
        self.cargar_grafo(nombre_base + '.gr')
        self.cargar_coordenadas(nombre_base + '.co')
    

    # Funcion que devuelve los vecinos (con sus costes) de un vertice pasado como argumento
    def obtener_sucesores(self, vertice):
        return self.adyacencia.get(vertice, [])
    

    # Funcion que calcula la distancia geodésica (linea recta sobre una esfera) entre dos vértices usando la fórmula de Haversine
    # Esta h es admisible porque la distancia estimada nunca será mayor que la distancia real por carretera
    def distancia_haversine(self, v1, v2):
        # v1: Identificador del primer vértice.
        # v2: Identificador del segundo vértice.
        
        # Se obtienen las coordenadas de los dos nodos
        lat1, lon1 = self.coordenadas[v1]
        lat2, lon2 = self.coordenadas[v2]
        
        # Se convierten a radianes para poder hacer operaciones trigonometricas con ellos
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        # Se aplica la formula de Haversine a los datos
        a = math.sin(delta_lat / 2) ** 2 + \
            math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        # Se convierte la distancia a metros multiplicando por el radio de la tierra y se devuelve la distancia final
        return self.RADIO_TIERRA * c
    

    # Funcion que verifica si existe un vertice en el grafo
    def existe_vertice(self, vertice):
        return vertice in self.coordenadas
    

