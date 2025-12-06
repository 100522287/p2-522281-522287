#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo para la implementación de la lista cerrada.

La lista cerrada (CLOSED) almacena los nodos ya expandidos en la búsqueda.
Su propósito principal es:
- Evitar la reexpansión de nodos (detección de duplicados)
- Almacenar información para reconstruir el camino solución

Se implementa mediante un diccionario que proporciona:
- Inserción: O(1) amortizado
- Búsqueda: O(1) amortizado
- Reconstrucción del camino: O(longitud del camino)
"""


class ListaCerrada:
    """
    Lista cerrada implementada como diccionario hash.
    
    Almacena para cada nodo expandido:
    - El nodo padre (para reconstruir el camino)
    - El coste del arco desde el padre (para verificar la solución)
    - El valor g (coste acumulado desde el inicio)
    
    Atributos:
        cerrados: Diccionario {nodo: (padre, coste_arco, g)}.
    """
    
    def __init__(self):
        """Inicializa una lista cerrada vacía."""
        self.cerrados = {}
    
    def insertar(self, nodo, padre, coste_arco, g):
        """
        Inserta un nodo en la lista cerrada.
        
        Args:
            nodo: Identificador del nodo expandido.
            padre: Identificador del nodo padre (None para el inicial).
            coste_arco: Coste del arco desde el padre hasta este nodo.
            g: Coste acumulado desde el inicio hasta este nodo.
        """
        self.cerrados[nodo] = (padre, coste_arco, g)
    
    def contiene(self, nodo):
        """
        Verifica si un nodo está en la lista cerrada.
        
        Args:
            nodo: Identificador del nodo.
            
        Returns:
            True si el nodo ha sido expandido, False en caso contrario.
        """
        return nodo in self.cerrados
    
    def obtener_padre(self, nodo):
        """
        Obtiene el padre de un nodo en la lista cerrada.
        
        Args:
            nodo: Identificador del nodo.
            
        Returns:
            Identificador del nodo padre, o None si es el nodo inicial.
        """
        if nodo in self.cerrados:
            padre, _, _ = self.cerrados[nodo]
            return padre
        return None
    
    def obtener_coste_arco(self, nodo):
        """
        Obtiene el coste del arco que llega a un nodo.
        
        Args:
            nodo: Identificador del nodo.
            
        Returns:
            Coste del arco desde el padre, o 0 si es el nodo inicial.
        """
        if nodo in self.cerrados:
            _, coste_arco, _ = self.cerrados[nodo]
            return coste_arco
        return 0
    
    def obtener_g(self, nodo):
        """
        Obtiene el valor g de un nodo en la lista cerrada.
        
        Args:
            nodo: Identificador del nodo.
            
        Returns:
            Valor g del nodo, o None si no está en la lista.
        """
        if nodo in self.cerrados:
            _, _, g = self.cerrados[nodo]
            return g
        return None
    
    def reconstruir_camino(self, nodo_objetivo):
        """
        Reconstruye el camino desde el inicio hasta el objetivo.
        
        Recorre los punteros de padre hacia atrás para obtener
        la secuencia de nodos y costes de arcos.
        
        Args:
            nodo_objetivo: Nodo final del camino.
            
        Returns:
            Lista de tuplas (nodo, coste_arco) desde el inicio hasta el objetivo.
            El primer elemento tiene coste_arco = 0.
        """
        camino = []
        nodo_actual = nodo_objetivo
        
        while nodo_actual is not None:
            coste_arco = self.obtener_coste_arco(nodo_actual)
            camino.append((nodo_actual, coste_arco))
            nodo_actual = self.obtener_padre(nodo_actual)
        
        # Invertir para obtener el camino desde el inicio
        camino.reverse()
        return camino
    
    def __len__(self):
        """Devuelve el número de nodos en la lista cerrada."""
        return len(self.cerrados)