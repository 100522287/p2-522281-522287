#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abierta import ListaAbierta


# Clase donde se implementa el algoritmo de A* usando una memoria "cache" de h(n)
class AlgoritmoAEstrella:
    
    def __init__(self, grafo, origen, destino):
        self.grafo = grafo # Objeto Grafo con el problema.
        self.origen = origen # Identificador del vértice de inicio.
        self.destino = destino # Identificador del vértice de destino.
        self.expansiones = 0 # numero de expansiones (al principio 0)
        self.coste_optimo = None # Será el coste del camino optimo
        # Se crea diccionario vacio para guardar los valores de la heuristica
        self.cache_h = {} # Lo hacemos para evitar calcular multiples veces la distiancia Haversine de un mismo nodo 
        # variables para las estadisticas
        self.hits_cache = 0  
        self.miss_cache = 0
    

    # Funcion que calcula la distancia Haversine (h(n)) desde el nodo actual, pasado como argumento, al nodo de destino
    def heuristica(self, nodo):
        # Se verifica primero si la h(n) ya está en caché
        if nodo in self.cache_h:
            self.hits_cache += 1
            # Se devuelve el valor guardado en el diccionario
            return self.cache_h[nodo]
        
        # Si no está en cache, calculamos la distancia llamando a la funcion distancia_haversine de la clase grafo
        self.miss_cache += 1 # sumamos uno ya que ha ocurrido un "fallo de caché"
        h = self.grafo.distancia_haversine(nodo, self.destino)
        # Se guarda en cache la distancia calculada (para que no se tenga que calcular más)
        self.cache_h[nodo] = h
        # Se devuelve la distancia calculada
        return h
    

    # Funcion que ejecuta el algoritmo A* para encontrar el camino más óptimo
    def resolver(self):

        # abierta es una instancia de la clase lista abierta.
        abierta = ListaAbierta()
        # Diccionario donde se guarda cada nodo con su mejor g(n) hasta el momento
        g_minimo = {self.origen: 0} # llegar al origen cuesta 0
        # Diccionario para reconstruir el camino, guarda qué padres tiene cada nodo
        padres = {self.origen: (None, 0)}
        # Diccionario que almacena el conjunto de nodos ya expandidos
        cerrada = set()
        
        # Se calcula la heuristica del nodo inicial respecto al nodo final
        h_origen = self.heuristica(self.origen)
        # Se inserta el nodo inicial en la lista abierta
        abierta.insertar(self.origen, 0, h_origen)
        
        # Bucle que se repite hasta que la lista abierta quede vacia
        while not abierta.esta_vacia():
            # Extraer nodo con menor f(n) de la lista abierta llamando a extraer_minimo
            resultado = abierta.extraer_minimo()
            # Si no hay minimo, algo ha fallado, no debería pasar
            if resultado is None:
                break
            # Obtenemos los datos de la tupla del resultado (nodo y g)
            nodo_actual, g_actual = resultado
            
            # Si el nodo actual es el de destino, ya hemos terminado
            if nodo_actual == self.destino:
                self.coste_optimo = g_actual # Coste optimo pasa a ser el g del resultado
                # Se llama a la funcion reconstruir camino para obtener el camino funal
                camino = self._reconstruir_camino(padres, nodo_actual)
                # Se devuelve tanto el camino final como el coste acumulado del camino
                return camino, g_actual
            
            # Si no hemos llegado al nodo de destino todavía, expandimos
            self.expansiones += 1
            # Metemos al nodo actual en la lista de nodos ya visitados
            cerrada.add(nodo_actual)
            
            # Expandimos para cada sucesor del nodo actual
            for sucesor, coste_arco in self.grafo.obtener_sucesores(nodo_actual):
                # Si el sucesor está en la lista cerrada ya, no se visita de nuevo
                if sucesor in cerrada:
                    continue
                
                # Se calcula el nuevo g sumándole el coste del arco
                g_sucesor = g_actual + coste_arco
                
                # Si encontramos un mejor camino
                if g_sucesor < g_minimo.get(sucesor, float('inf')):
                    # Actualizamos el coste
                    g_minimo[sucesor] = g_sucesor
                    # Guardamos en la lista de padres que venimos del nodo actual para ir al sucesor
                    padres[sucesor] = (nodo_actual, coste_arco)
                    
                    # Se obtiene la heuristica del sucesor llamando a la funcion heuristica
                    h_sucesor = self.heuristica(sucesor)
                    # Insertamos (o actualizamos) el sucesor en la lista abierta con su nuevo coste y heuristica
                    abierta.insertar(sucesor, g_sucesor, h_sucesor)
        
        # No se encontró solución
        return None, None
    

    # Funcion que reconstruye el camino desde el origen hasta el objetivo
    def _reconstruir_camino(self, padres, nodo_objetivo):

        camino = [] # lista que se devolvera y contendrá los nodos ordenados
        nodo_actual = nodo_objetivo # Se empieza por el final
        
        # Bucle while que va retrocediendo hasta el inicio
        # El nodo inicial se habrá guardado con padre = none, lo que detendrá el bucle
        while nodo_actual is not None:
            # Se recupera el padre y el costo_arco del nodo actual
            padre, coste_arco = padres[nodo_actual]
            # Se añade al camino la tupla nodo, coste
            camino.append((nodo_actual, coste_arco))
            # Nodo actual pasa a ser el padre del nodo actual
            nodo_actual = padre
        
        # Invertir para obtener el camino desde el principio
        camino.reverse()
        # Se retorna la lista con todas las tuplas ordenadas
        return camino
    

    # Funcion que obtiene estadisticas del uso del diccionario cache
    def obtener_estadisticas_cache(self):

        total = self.hits_cache + self.miss_cache
        ratio = self.hits_cache / total if total > 0 else 0
        
        return {
            'hits': self.hits_cache, # Numero de aciertos
            'misses': self.miss_cache, # Numero de fallos
            'total': total, # Numero de aciertos + numero de fallos 
            'hit_ratio': ratio, # hit ratio
            'ahorro_calculos': f"{ratio*100:.1f}%" # porcentaje de ahorro al implementar la "cache"
        }



# Implementacion del algoritmo de Dijktra
class AlgoritmoDijkstra:
    def __init__(self, grafo, origen, destino):
        
        self.grafo = grafo # Objeto Grafo con el problema.
        self.origen = origen # Identificador del vértice de inicio.
        self.destino = destino # Identificador del vértice objetivo.
        self.expansiones = 0 # numero de expansiones (al principio 0)
        self.coste_optimo = None # Será el coste acumulado del camino optimo
    

    # Funcion que ejecuta el algoritmo de dijkstra
    def resolver(self):
        # abierta es una instancia de la clase lista abierta.
        abierta = ListaAbierta()
        # Diccionario donde se guarda cada nodo con su mejor g(n) hasta el momento
        g_minimo = {self.origen: 0} # llegar al origen cuesta 0
        # Diccionario para reconstruir el camino, guarda qué padres tiene cada nodo
        padres = {self.origen: (None, 0)}
        # Diccionario que almacena el conjunto de nodos ya expandidos
        cerrada = set()
        
        # h=0 para Dijkstra, puesto que no se utilizan heuristicas
        # Se inserta el nodo inicial en la lista abierta
        abierta.insertar(self.origen, 0, 0)
        
        # Bucle que se repite hasta que la lista abierta quede vacia
        while not abierta.esta_vacia():
            # Extraer nodo con menor f(n) de la lista abierta llamando a extraer_minimo
            resultado = abierta.extraer_minimo()
            # Si no hay minimo, algo ha fallado, no debería pasar
            if resultado is None:
                break
            # Obtenemos los datos de la tupla del resultado (nodo y g)
            nodo_actual, g_actual = resultado
            
            # Si el nodo actual es el de destino, ya hemos terminado
            if nodo_actual == self.destino:
                self.coste_optimo = g_actual # Coste optimo pasa a ser el g del resultado
                # Se llama a la funcion reconstruir camino para obtener el camino final
                camino = self._reconstruir_camino(padres, nodo_actual)
                # Se devuelve tanto el camino final como el coste acumulado del camino
                return camino, g_actual
            
            # Si no hemos llegado al nodo de destino todavía, expandimos
            self.expansiones += 1
            # Metemos al nodo actual en la lista de nodos ya visitados
            cerrada.add(nodo_actual)
            
            # Expandimos para cada sucesor del nodo actual
            for sucesor, coste_arco in self.grafo.obtener_sucesores(nodo_actual):
                # Si el sucesor está en la lista cerrada ya, no se visita de nuevo
                if sucesor in cerrada:
                    continue
                
                # Se calcula el nuevo g sumándole el coste del arco
                g_sucesor = g_actual + coste_arco
                
                # Si encontramos un mejor camino
                if g_sucesor < g_minimo.get(sucesor, float('inf')):
                    # Actualizamos el coste
                    g_minimo[sucesor] = g_sucesor
                    # Guardamos en la lista de padres que venimos del nodo actual para ir al sucesor
                    padres[sucesor] = (nodo_actual, coste_arco)
                    # Insertamos (o actualizamos) el sucesor en la lista abierta con su nuevo coste y heuristica
                    abierta.insertar(sucesor, g_sucesor, 0)
        
        # Si hemos llegado hasta aquí, no se encontró solucion
        return None, None
    

    # Funcion que reconstruye el camino desde el origen hasta el objetivo
    def _reconstruir_camino(self, padres, nodo_objetivo):

        camino = [] # lista que se devolvera y contendrá los nodos ordenados
        nodo_actual = nodo_objetivo # Se empieza por el final
        
        # Bucle while que va retrocediendo hasta el inicio
        # El nodo inicial se habrá guardado con padre = none, lo que detendrá el bucle
        while nodo_actual is not None:
            # Se recupera el padre y el costo_arco del nodo actual
            padre, coste_arco = padres[nodo_actual]
            # Se añade al camino la tupla nodo, coste
            camino.append((nodo_actual, coste_arco))
            # Nodo actual pasa a ser el padre del nodo actual
            nodo_actual = padre
        
        # Invertir para obtener el camino desde el principio
        camino.reverse()
        # Se retorna la lista con todas las tuplas ordenadas
        return camino


