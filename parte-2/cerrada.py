#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Clase donde se implementa una lista cerrada, necesaria po¡ara los algoritmos de A* y Diskstra
# Se utiliza un diccionario hash en vez de una lista, lo que hace la lista cerrada mucho más eficiente
class ListaCerrada:
    
    def __init__(self):
        self.cerrados = {} # Diccionario donde se almacenaran los nodos que ya han sido visitados
    
    # Funcion que inserta el nodo en la lista cerrados
    def insertar(self, nodo, padre, coste_arco, g):
        # nodo: Identificador del nodo expandido.
        # padre: Identificador del nodo padre, para reconstruir el camino luego (None para el inicial).
        # coste_arco: Coste del arco desde el padre hasta este nodo.
        # g: Coste acumulado desde el inicio hasta este nodo.
        
        # Se asigna la entrada en el diccionario (el nodo será la clave y el valor una tupla de padre, coste_arco y g)
        self.cerrados[nodo] = (padre, coste_arco, g)
    

    # Funcion que verifica si el nodo que se pasa como argumento está en la lista cerrada
    def contiene(self, nodo):
        return nodo in self.cerrados
    

    # Funcion que obtiene el padre (almacenado en las tuplas) del nodo pasado como argumento
    def obtener_padre(self, nodo):
        # Verifica que el nodo esté en la lista cerrados
        if nodo in self.cerrados:
            # Obtiene el padre del nodo ignorando los demás valores de la tupla
            padre, _, _ = self.cerrados[nodo]
            return padre
        # Si el nodo no está en la lista. no retorna nada
        return None
    

    # Funcion que obtiene el coste_arco (almacenado en las tuplas) del nodo pasado como argumento
    def obtener_coste_arco(self, nodo):
        # Verifica que el nodo esté en la lista cerrados
        if nodo in self.cerrados:
            # Obtiene el coste_arco del nodo ignorando los demás valores de la tupla
            _, coste_arco, _ = self.cerrados[nodo]
            return coste_arco
        # Si el nodo no está en la lista. retorna un 0
        return 0
    

    # Funcion que obtiene el g (almacenado en las tuplas) del nodo pasado como argumento
    def obtener_g(self, nodo):
        # Verifica que el nodo esté en la lista cerrados
        if nodo in self.cerrados:
            # Obtiene el g del nodo ignorando los demás valores de la tupla
            _, _, g = self.cerrados[nodo]
            return g
        # Si el nodo no está en la lista. no retorna nada
        return None
    

    # Funcion que reconstruye el camino desde el nodo inicial hasta el nodo objetivo (pasado como argumento) 
    def reconstruir_camino(self, nodo_objetivo):
        # Se crea una lista vacia para almacenar la secuencia de nodos
        camino = []
        # Se empieza por el nodo final, y se va reconstruyendo hasta el nodo inicial
        nodo_actual = nodo_objetivo
        
        # Bucle while que va retrocediendo hasta el inicio
        # El nodo inicial se habrá guardado con padre = none, lo que detendrá el bucle 
        while nodo_actual is not None:
            # Se recupera cuanto costó llegar hasta este nodo desde su padre
            coste_arco = self.obtener_coste_arco(nodo_actual)
            # Se añade al camino la tupla nodo, coste
            camino.append((nodo_actual, coste_arco))
            # Nodo actual pasa a ser el padre del nodo actual
            nodo_actual = self.obtener_padre(nodo_actual)
        
        # Invertir para obtener el camino desde el inicio
        camino.reverse()
        # Se retorna la lista con todas las tuplas ordenadas
        return camino
    
    # Devuelve el número de nodos en la lista cerrada.
    def __len__(self):
        return len(self.cerrados)
    
