#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Clase que implementa toda la logica necesaria para una lista abierta que se usa en los algoritmos de A* y Dikstra
# Se implementa con dial's bucket en con set() en vez de con una lista normal para aumentar la eficiencia de las actualizaciones
# Sus funciones principales son insertar y extraer_minimo, aunque tambien contiene funciones secundarias
class ListaAbierta:
    
    def __init__(self):
        self.buckets = {}  # Diccionario donde las claves son el coste f y los valores son los nodos que tienen esa f
        self.entrada = {}  # Diccionario auxiliar para comprobar si un nodo esta en la lista
        self.min_f = float('inf') # la variable que rastrea el valor minimo de f se inicializa como infinito
    

    # Funcion que permite insertar un nuevo nodo o actualizar uno existente si 
    # ha encontrado un camino mejor.
    def insertar(self, nodo, g, h):
        # nodo: Identificador del nodo.
        # g: Coste del camino desde el inicio hasta el nodo.
        # h: Valor heurístico desde el nodo hasta el objetivo.
        
        # Se calcula la prioridad f del nodo sumando su coste acumulado desde el inicio y su heuristica
        f = int(g + h)  # Asegurar que f es entero para indexar buckets
        
        # Comprobamos si el nodo ya existe en la lista de entrada
        if nodo in self.entrada:
            # Si existe en entrada, cogemos los valores del nodo en la lista
            f_anterior, g_anterior = self.entrada[nodo]
            
            # Si el coste del camino de la lista es mejor que el nuevo, no hacemos nada
            if g_anterior <= g:
                return
            
            # Verificamos que el bucket antiguo exista
            if f_anterior in self.buckets:
                # se eliminina el nodo antiguo del buvket antiguo 
                self.buckets[f_anterior].discard(nodo)  # Se utiliza discard en vez de buscar en una lista porque es más rapido O(1)
                
                # Si el bucket queda vacío tras eliminar el nodo antiguo, lo eliminamos
                if not self.buckets[f_anterior]:
                    del self.buckets[f_anterior]
                    # Si era el mínimo, recalcular
                    if f_anterior == self.min_f:
                        # Si quedan buckets buscamos el nuevo minimo, y si no lo encontramos, volvemos a infinito
                        if self.buckets:
                            self.min_f = min(self.buckets.keys())
                        else:
                            self.min_f = float('inf')
        
        # Si el nodo no exiete en la lista de entradas:
        # Si no existe un bucket f, se crea para poder almacenar l nuevo nodo
        if f not in self.buckets:
            self.buckets[f] = set()  # Se usa set en lugar de deque porque es mas eficiente
        
        # Se almacena el nuevo nodo tanto en buckets como en entrada
        self.buckets[f].add(nodo)  # Se usa add en lugar de append porque es mas eficiente
        self.entrada[nodo] = (f, g)
        
        # Se actualiza el min_f si es necesario
        if f < self.min_f:
            self.min_f = f
    

    # Funcion que extrae el nodo con el menor coste f para expandirlo
    def extraer_minimo(self):
        # Si buckets está vacio, se devuelve none, ya que no hay nada que devolver
        if not self.buckets:
            return None
        
        # Bucle while para asegurar que encontramos un nodo usando min_f
        while self.min_f in self.buckets:
            # Obtiene todos los nodos cuya f sea la minima
            bucket = self.buckets[self.min_f]

            # Si el bucket tiene elementos:
            if bucket:
                # Se extrae uno de los nodos contenidos en el bucket
                nodo = bucket.pop()  # O(1) con set.pop()
                
                # Si tras sacar el nodo anterior el bucket queda vacío, se elimina
                if not bucket:
                    del self.buckets[self.min_f]
                
                # Obtener el g del diccionario y eliminar entrada
                if nodo in self.entrada:
                    _, g = self.entrada[nodo]
                    del self.entrada[nodo]
                    
                    # Actualizar min_f en el caso de que fuese necesario
                    if not self.buckets:
                        self.min_f = float('inf')
                    elif self.min_f not in self.buckets:
                        self.min_f = min(self.buckets.keys())
                    
                    # Al final, se devuelve el nodo y su coste acumulado g
                    return nodo, g
            
            # Si el bucket está vacio, se elimina de la lista, aunque esto no deberia pasar
            del self.buckets[self.min_f]
            # Se actualiza min_f en base a si existe el diccionario buckets tras eliminar el nodo anterior
            if self.buckets:
                self.min_f = min(self.buckets.keys())
            else:
                self.min_f = float('inf')
                break
        
        # Si no se ha encontrado nada, no se devuelve nada
        return None
    
    # Funcion que verifica si la lista abierta está vacia 
    def esta_vacia(self):
        return len(self.entrada) == 0
    
    # Funcion que verifica si una lis
    def contiene(self, nodo):
        return nodo in self.entrada
    
    # Funcion que obtiene el valor del coste acumulado g de un nodo en la lista abierta
    def obtener_g(self, nodo):
        if nodo in self.entrada:
            _, g = self.entrada[nodo]
            return g
        return None
    
    # Funcion que devuelve el numero de nodos de la lista abierta
    def __len__(self):
        return len(self.entrada)