#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo para la implementación de la lista abierta usando Dial's Bucket.

Dial's Algorithm (1969) es una optimización para el algoritmo de Dijkstra
cuando los pesos de los arcos son enteros no negativos y acotados.

En lugar de usar un heap binario, utiliza un array de "buckets" (cubos)
donde cada bucket i contiene los nodos con valor f(n) = i.

Complejidad:
- Inserción: O(1)
- Extracción del mínimo: O(C) amortizado, donde C es el coste máximo de un arco
- Actualización: O(1)

Esta estructura es especialmente eficiente para los grafos DIMACS donde
los costes son distancias en metros (enteros relativamente pequeños comparados
con el número de nodos).
"""

from collections import deque


class ListaAbierta:
    """
    Lista abierta implementada con Dial's Bucket.
    
    Utiliza un array circular de buckets indexados por el valor f(n).
    Cada bucket es una cola (deque) de nodos con el mismo valor f.
    
    Atributos:
        buckets: Diccionario de buckets {f: deque de (nodo, g)}.
        entrada: Diccionario para acceso rápido {nodo: (f, g)}.
        min_f: Valor f mínimo actual en la estructura.
        num_elementos: Número de elementos válidos en la estructura.
    """
    
    def __init__(self):
        """Inicializa una lista abierta vacía."""
        self.buckets = {}  # {f: deque de (nodo, g)}
        self.entrada = {}  # {nodo: (f, g)}
        self.min_f = float('inf')
        self.num_elementos = 0
    
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
        f = int(g + h)  # Asegurar que f es entero para indexar buckets
        
        # Si el nodo ya existe, verificar si debemos actualizar
        if nodo in self.entrada:
            f_anterior, g_anterior = self.entrada[nodo]
            if g_anterior <= g:
                return  # El valor existente es mejor o igual, ignorar
            
            # Eliminar la entrada anterior del bucket (lazy deletion)
            # No eliminamos físicamente, solo actualizamos el diccionario
            self.num_elementos -= 1
        
        # Insertar en el bucket correspondiente
        if f not in self.buckets:
            self.buckets[f] = deque()
        
        self.buckets[f].append((nodo, g))
        self.entrada[nodo] = (f, g)
        self.num_elementos += 1
        
        # Actualizar mínimo
        if f < self.min_f:
            self.min_f = f
    
    def extraer_minimo(self):
        """
        Extrae y devuelve el nodo con menor valor f(n).
        
        Busca el bucket con menor índice que contenga nodos válidos.
        Utiliza lazy deletion: salta las entradas que ya no son válidas.
        
        Returns:
            Tupla (nodo, g) del nodo con menor f, o None si la lista está vacía.
        """
        if self.num_elementos == 0:
            return None
        
        # Buscar el bucket no vacío con menor f
        # Empezamos desde min_f y avanzamos
        while self.min_f in self.buckets or self.min_f < float('inf'):
            if self.min_f not in self.buckets:
                # Buscar el siguiente bucket existente
                if not self.buckets:
                    return None
                self.min_f = min(self.buckets.keys())
            
            bucket = self.buckets[self.min_f]
            
            while bucket:
                nodo, g = bucket.popleft()
                
                # Verificar si esta entrada sigue siendo válida
                if nodo in self.entrada:
                    f_guardado, g_guardado = self.entrada[nodo]
                    if f_guardado == self.min_f and g == g_guardado:
                        # Entrada válida, eliminar del diccionario y devolver
                        del self.entrada[nodo]
                        self.num_elementos -= 1
                        return nodo, g
            
            # Bucket vacío, eliminarlo y buscar el siguiente
            del self.buckets[self.min_f]
            
            if self.buckets:
                self.min_f = min(self.buckets.keys())
            else:
                self.min_f = float('inf')
                break
        
        return None
    
    def esta_vacia(self):
        """
        Verifica si la lista abierta está vacía.
        
        Returns:
            True si no hay nodos válidos en la lista.
        """
        return self.num_elementos == 0
    
    def contiene(self, nodo):
        """
        Verifica si un nodo está en la lista abierta.
        
        Args:
            nodo: Identificador del nodo.
            
        Returns:
            True si el nodo está en la lista.
        """
        return nodo in self.entrada
    
    def obtener_g(self, nodo):
        """
        Obtiene el valor g de un nodo en la lista abierta.
        
        Args:
            nodo: Identificador del nodo.
            
        Returns:
            Valor g del nodo, o None si no está en la lista.
        """
        if nodo in self.entrada:
            _, g = self.entrada[nodo]
            return g
        return None
    
    def __len__(self):
        """Devuelve el número de nodos válidos en la lista."""
        return self.num_elementos


class ListaAbiertaDialOptimizada:
    """
    Versión optimizada de Dial's Bucket con array circular.
    
    Esta versión utiliza un array de tamaño fijo (basado en el coste máximo
    de arco) y lo recorre de forma circular para encontrar el mínimo.
    
    Es más eficiente en memoria cuando el rango de valores f es conocido
    y acotado.
    
    Atributos:
        C: Coste máximo de un arco (determina el tamaño del array circular).
        buckets: Lista de sets, cada uno conteniendo nodos con ese valor f mod (C+1).
        entrada: Diccionario {nodo: (f, g)} para acceso rápido.
        puntero: Índice actual para búsqueda circular.
        num_elementos: Número de elementos en la estructura.
    """
    
    def __init__(self, coste_maximo_arco):
        """
        Inicializa la lista abierta con Dial's Bucket circular.
        
        Args:
            coste_maximo_arco: Coste máximo de cualquier arco en el grafo.
        """
        # El tamaño del array circular es C+1 donde C es el coste máximo
        self.C = coste_maximo_arco
        self.tamanio = self.C + 1
        self.buckets = [set() for _ in range(self.tamanio)]
        self.entrada = {}  # {nodo: (f, g)}
        self.puntero = 0
        self.num_elementos = 0
    
    def insertar(self, nodo, g, h):
        """
        Inserta un nodo en la lista abierta.
        
        Args:
            nodo: Identificador del nodo.
            g: Coste desde el inicio.
            h: Valor heurístico.
        """
        f = int(g + h)
        
        if nodo in self.entrada:
            f_anterior, g_anterior = self.entrada[nodo]
            if g_anterior <= g:
                return
            # Eliminar de bucket anterior
            indice_anterior = f_anterior % self.tamanio
            self.buckets[indice_anterior].discard(nodo)
            self.num_elementos -= 1
        
        # Insertar en nuevo bucket
        indice = f % self.tamanio
        self.buckets[indice].add(nodo)
        self.entrada[nodo] = (f, g)
        self.num_elementos += 1
    
    def extraer_minimo(self):
        """
        Extrae el nodo con menor f.
        
        Returns:
            Tupla (nodo, g) o None si está vacía.
        """
        if self.num_elementos == 0:
            return None
        
        # Buscar el siguiente bucket no vacío
        for _ in range(self.tamanio):
            if self.buckets[self.puntero]:
                nodo = self.buckets[self.puntero].pop()
                f, g = self.entrada[nodo]
                del self.entrada[nodo]
                self.num_elementos -= 1
                return nodo, g
            self.puntero = (self.puntero + 1) % self.tamanio
        
        return None
    
    def esta_vacia(self):
        """Verifica si está vacía."""
        return self.num_elementos == 0
    
    def contiene(self, nodo):
        """Verifica si contiene un nodo."""
        return nodo in self.entrada
    
    def obtener_g(self, nodo):
        """Obtiene el valor g de un nodo."""
        if nodo in self.entrada:
            _, g = self.entrada[nodo]
            return g
        return None
    
    def __len__(self):
        """Número de elementos."""
        return self.num_elementos