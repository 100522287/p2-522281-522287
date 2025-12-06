#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo para la lectura y representación eficiente de grafos DIMACS.

Este módulo implementa una clase Graph que permite:
- Leer ficheros de grafo (.gr) con arcos y distancias
- Leer ficheros de coordenadas (.co) con longitud y latitud
- Representar el grafo mediante listas de adyacencia
- Calcular distancias geodésicas entre vértices

La representación mediante listas de adyacencia proporciona:
- Acceso O(1) a los vecinos de un vértice
- Consumo de memoria O(V + E)
"""

import math


class Grafo:
    """
    Representación de un grafo dirigido ponderado con coordenadas geográficas.
    
    Atributos:
        num_vertices: Número de vértices en el grafo.
        num_arcos: Número de arcos en el grafo.
        adyacencia: Diccionario de listas de adyacencia {v: [(u, coste), ...]}.
        coordenadas: Diccionario de coordenadas {v: (latitud, longitud)}.
    """
    
    # Radio de la Tierra en metros para el cálculo de distancias geodésicas
    RADIO_TIERRA = 6371000
    
    def __init__(self):
        """Inicializa un grafo vacío."""
        self.num_vertices = 0
        self.num_arcos = 0
        self.adyacencia = {}
        self.coordenadas = {}
    
    def cargar_grafo(self, fichero_gr):
        """
        Carga la estructura del grafo desde un fichero .gr de DIMACS.
        
        El formato esperado es:
        - Líneas que comienzan con 'a': a <id1> <id2> <coste>
        - El resto de líneas se ignoran.
        
        Args:
            fichero_gr: Ruta al fichero de grafo.
        """
        with open(fichero_gr, 'r') as f:
            for linea in f:
                partes = linea.strip().split()
                if len(partes) >= 4 and partes[0] == 'a':
                    origen = int(partes[1])
                    destino = int(partes[2])
                    coste = int(partes[3])
                    
                    # Inicializar lista de adyacencia si no existe
                    if origen not in self.adyacencia:
                        self.adyacencia[origen] = []
                    
                    # Añadir arco (destino, coste)
                    self.adyacencia[origen].append((destino, coste))
                    self.num_arcos += 1
    
    def cargar_coordenadas(self, fichero_co):
        """
        Carga las coordenadas geográficas desde un fichero .co de DIMACS.
        
        El formato esperado es:
        - Líneas que comienzan con 'v': v <id> <longitud> <latitud>
        - Las coordenadas están multiplicadas por 10^6.
        - El resto de líneas se ignoran.
        
        Args:
            fichero_co: Ruta al fichero de coordenadas.
        """
        with open(fichero_co, 'r') as f:
            for linea in f:
                partes = linea.strip().split()
                if len(partes) >= 4 and partes[0] == 'v':
                    vertice = int(partes[1])
                    # Las coordenadas vienen multiplicadas por 10^6
                    longitud = int(partes[2]) / 1e6
                    latitud = int(partes[3]) / 1e6
                    
                    # Almacenar coordenadas (latitud, longitud)
                    self.coordenadas[vertice] = (latitud, longitud)
                    self.num_vertices += 1
    
    def cargar(self, nombre_base):
        """
        Carga el grafo completo (estructura y coordenadas).
        
        Args:
            nombre_base: Nombre base del grafo (sin extensión).
                         Se añadirán automáticamente .gr y .co
        """
        self.cargar_grafo(nombre_base + '.gr')
        self.cargar_coordenadas(nombre_base + '.co')
    
    def obtener_sucesores(self, vertice):
        """
        Obtiene los sucesores de un vértice con sus costes.
        
        Args:
            vertice: Identificador del vértice.
            
        Returns:
            Lista de tuplas (sucesor, coste) o lista vacía si no tiene sucesores.
        """
        return self.adyacencia.get(vertice, [])
    
    def distancia_haversine(self, v1, v2):
        """
        Calcula la distancia geodésica entre dos vértices usando la fórmula de Haversine.
        
        Esta distancia representa el camino más corto sobre la superficie de la Tierra
        (arco de círculo máximo) y es una heurística admisible porque cualquier
        camino por carretera tendrá una distancia mayor o igual.
        
        Args:
            v1: Identificador del primer vértice.
            v2: Identificador del segundo vértice.
            
        Returns:
            Distancia en metros entre los dos vértices.
        """
        lat1, lon1 = self.coordenadas[v1]
        lat2, lon2 = self.coordenadas[v2]
        
        # Convertir a radianes
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        # Fórmula de Haversine
        a = math.sin(delta_lat / 2) ** 2 + \
            math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return self.RADIO_TIERRA * c
    
    def existe_vertice(self, vertice):
        """
        Verifica si un vértice existe en el grafo.
        
        Args:
            vertice: Identificador del vértice.
            
        Returns:
            True si el vértice existe, False en caso contrario.
        """
        return vertice in self.coordenadas