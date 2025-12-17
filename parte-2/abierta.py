#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo para la implementación de la lista abierta usando Dial's Bucket.

VERSIÓN SIN LAZY DELETION - Más eficiente y limpia.

Dial's Algorithm (1969) es una optimización para el algoritmo de Dijkstra
cuando los pesos de los arcos son enteros no negativos y acotados.

En lugar de usar un heap binario, utiliza un array de "buckets" (cubos)
donde cada bucket i contiene los nodos con valor f(n) = i.

Complejidad:
- Inserción: O(1)
- Extracción del mínimo: O(C) amortizado, donde C es el coste máximo de un arco
- Actualización: O(1) con eliminación explícita del bucket anterior

Esta estructura es especialmente eficiente para los grafos DIMACS donde
los costes son distancias en metros (enteros relativamente pequeños comparados
con el número de nodos).
"""

from collections import deque


class ListaAbierta:
    """
    Lista abierta implementada con Dial's Bucket SIN lazy deletion.
    
    Utiliza un diccionario de buckets indexados por el valor f(n).
    Cada bucket es una cola (deque) de nodos con el mismo valor f.
    
    Cuando actualizamos un nodo, LO ELIMINAMOS EXPLÍCITAMENTE del bucket
    anterior antes de insertarlo en el nuevo. Esto evita el overhead de
    lazy deletion y hace la estructura más eficiente.
    
    Atributos:
        buckets: Diccionario de buckets {f: deque de nodos}.
        entrada: Diccionario para acceso rápido {nodo: (f, g)}.
        min_f: Valor f mínimo actual en la estructura.
    """
    
    def __init__(self):
        """Inicializa una lista abierta vacía."""
        self.buckets = {}  # {f: deque de nodos}
        self.entrada = {}  # {nodo: (f, g)}
        self.min_f = float('inf')
    
    def insertar(self, nodo, g, h):
        """
        Inserta un nodo en la lista abierta o actualiza su valor si ya existe.
        
        Si el nodo ya está en la lista con un valor g mayor, se actualiza
        eliminándolo explícitamente del bucket anterior.
        
        Args:
            nodo: Identificador del nodo.
            g: Coste del camino desde el inicio hasta el nodo.
            h: Valor heurístico desde el nodo hasta el objetivo.
        """
        f = int(g + h)  # Asegurar que f es entero para indexar buckets
        
        # Si el nodo ya existe, verificar si debemos actualizar
        if nodo in self.entrada:
            f_anterior, g_anterior = self.entrada[nodo]
            
            # Si el nuevo g no es mejor, ignorar
            if g_anterior <= g:
                return
            
            # ELIMINACIÓN EXPLÍCITA: quitar del bucket anterior
            if f_anterior in self.buckets:
                try:
                    self.buckets[f_anterior].remove(nodo)
                    # Si el bucket queda vacío, eliminarlo
                    if not self.buckets[f_anterior]:
                        del self.buckets[f_anterior]
                        # Si era el mínimo, recalcular
                        if f_anterior == self.min_f:
                            if self.buckets:
                                self.min_f = min(self.buckets.keys())
                            else:
                                self.min_f = float('inf')
                except ValueError:
                    # El nodo no estaba en el bucket (no debería pasar)
                    pass
        
        # Insertar en el bucket correspondiente
        if f not in self.buckets:
            self.buckets[f] = deque()
        
        self.buckets[f].append(nodo)
        self.entrada[nodo] = (f, g)
        
        # Actualizar mínimo
        if f < self.min_f:
            self.min_f = f
    
    def extraer_minimo(self):
        """
        Extrae y devuelve el nodo con menor valor f(n).
        
        Como no hay lazy deletion, el primer nodo que encontramos
        en el bucket mínimo es válido.
        
        Returns:
            Tupla (nodo, g) del nodo con menor f, o None si la lista está vacía.
        """
        if not self.buckets:
            return None
        
        # El bucket con min_f debe existir y no estar vacío
        while self.min_f in self.buckets:
            bucket = self.buckets[self.min_f]
            
            if bucket:
                nodo = bucket.popleft()
                
                # Si el bucket queda vacío, eliminarlo
                if not bucket:
                    del self.buckets[self.min_f]
                
                # Obtener el g del diccionario y eliminar entrada
                if nodo in self.entrada:
                    _, g = self.entrada[nodo]
                    del self.entrada[nodo]
                    
                    # Actualizar min_f si es necesario
                    if not self.buckets:
                        self.min_f = float('inf')
                    elif self.min_f not in self.buckets:
                        self.min_f = min(self.buckets.keys())
                    
                    return nodo, g
            
            # Bucket vacío (no debería pasar), eliminarlo y continuar
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
            True si no hay nodos en la lista.
        """
        return len(self.entrada) == 0
    
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
        """Devuelve el número de nodos en la lista."""
        return len(self.entrada)