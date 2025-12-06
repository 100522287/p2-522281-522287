#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo para la implementación de la lista abierta.

La lista abierta (OPEN) es una estructura de datos fundamental en los
algoritmos de búsqueda heurística como A*. Debe soportar eficientemente:
- Inserción de nodos con su valor f(n) = g(n) + h(n)
- Extracción del nodo con menor valor f(n)
- Actualización del valor de un nodo existente

Se implementa mediante un heap binario (heapq) que proporciona:
- Inserción: O(log n)
- Extracción del mínimo: O(log n)
- Actualización: O(log n) con lazy deletion
"""

import heapq


class ListaAbierta:
    """
    Lista abierta implementada como cola de prioridad con lazy deletion.
    
    Utiliza un heap binario para mantener los nodos ordenados por f(n).
    La técnica de lazy deletion permite manejar eficientemente las
    actualizaciones de valores sin necesidad de reordenar el heap.
    
    Atributos:
        heap: Lista que implementa el heap binario.
        entrada: Diccionario para acceso rápido {nodo: (f, g, entrada_válida)}.
        contador: Contador para desempate en el heap.
    """
    
    def __init__(self):
        """Inicializa una lista abierta vacía."""
        self.heap = []
        self.entrada = {}
        self.contador = 0
    
    def insertar(self, nodo, g, h):
        """
        Inserta un nodo en la lista abierta o actualiza su valor si ya existe.
        
        Si el nodo ya está en la lista con un valor g mayor, se actualiza.
        Si tiene un valor g menor o igual, se ignora la inserción.
        
        Args:
            nodo: Identificador del nodo.
            g: Coste del camino desde el inicio hasta el nodo.
            h: Valor heurístico desde el nodo hasta el objetivo.
        """
        f = g + h
        
        # Si el nodo ya existe y tiene mejor g, ignorar
        if nodo in self.entrada:
            _, g_anterior, valido = self.entrada[nodo]
            if valido and g_anterior <= g:
                return
            # Marcar la entrada anterior como inválida (lazy deletion)
            self.entrada[nodo] = (f, g_anterior, False)
        
        # Insertar nueva entrada
        self.contador += 1
        entrada = (f, self.contador, nodo, g)
        self.entrada[nodo] = (f, g, True)
        heapq.heappush(self.heap, entrada)
    
    def extraer_minimo(self):
        """
        Extrae y devuelve el nodo con menor valor f(n).
        
        Utiliza lazy deletion: salta las entradas marcadas como inválidas.
        
        Returns:
            Tupla (nodo, g) del nodo con menor f, o None si la lista está vacía.
        """
        while self.heap:
            f, _, nodo, g = heapq.heappop(self.heap)
            
            # Verificar si esta entrada sigue siendo válida
            if nodo in self.entrada:
                f_guardado, g_guardado, valido = self.entrada[nodo]
                if valido and g == g_guardado:
                    # Eliminar del diccionario de entradas
                    del self.entrada[nodo]
                    return nodo, g
        
        return None
    
    def esta_vacia(self):
        """
        Verifica si la lista abierta está vacía.
        
        Returns:
            True si no hay nodos válidos en la lista.
        """
        # Verificar si hay alguna entrada válida
        for _, (_, _, valido) in self.entrada.items():
            if valido:
                return False
        return True
    
    def contiene(self, nodo):
        """
        Verifica si un nodo está en la lista abierta.
        
        Args:
            nodo: Identificador del nodo.
            
        Returns:
            True si el nodo está en la lista y su entrada es válida.
        """
        if nodo in self.entrada:
            _, _, valido = self.entrada[nodo]
            return valido
        return False
    
    def obtener_g(self, nodo):
        """
        Obtiene el valor g de un nodo en la lista abierta.
        
        Args:
            nodo: Identificador del nodo.
            
        Returns:
            Valor g del nodo, o None si no está en la lista.
        """
        if nodo in self.entrada:
            _, g, valido = self.entrada[nodo]
            if valido:
                return g
        return None
    
    def __len__(self):
        """Devuelve el número de nodos válidos en la lista."""
        return sum(1 for _, (_, _, valido) in self.entrada.items() if valido)