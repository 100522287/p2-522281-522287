#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo con la implementación del algoritmo de búsqueda A*.

A* es un algoritmo de búsqueda informada que combina:
- g(n): coste del camino desde el inicio hasta n
- h(n): estimación heurística del coste desde n hasta el objetivo
- f(n) = g(n) + h(n): función de evaluación

Propiedades de A*:
- Es ADMISIBLE: garantiza encontrar la solución óptima si h(n) es admisible
  (nunca sobreestima el coste real)
- Es ÓPTIMAMENTE EFICIENTE: ningún otro algoritmo admisible expande menos nodos
  con la misma heurística

La heurística utilizada es la distancia geodésica (Haversine), que es admisible
porque representa el camino más corto posible sobre la superficie terrestre.
"""

from abierta import ListaAbierta
from cerrada import ListaCerrada


class AlgoritmoAStar:
    """
    Implementación del algoritmo A* para el problema del camino más corto.
    
    Atributos:
        grafo: Objeto Grafo con la estructura del problema.
        origen: Vértice de inicio.
        destino: Vértice objetivo.
        abierta: Lista abierta (cola de prioridad).
        cerrada: Lista cerrada (nodos expandidos).
        expansiones: Contador de nodos expandidos.
        coste_optimo: Coste de la solución óptima encontrada.
    """
    
    def __init__(self, grafo, origen, destino):
        """
        Inicializa el algoritmo A*.
        
        Args:
            grafo: Objeto Grafo con el problema.
            origen: Identificador del vértice de inicio.
            destino: Identificador del vértice objetivo.
        """
        self.grafo = grafo
        self.origen = origen
        self.destino = destino
        self.abierta = ListaAbierta()
        self.cerrada = ListaCerrada()
        self.expansiones = 0
        self.coste_optimo = None
    
    def heuristica(self, nodo):
        """
        Calcula el valor heurístico h(n) para un nodo.
        
        Utiliza la distancia geodésica (Haversine) como heurística.
        Esta heurística es ADMISIBLE porque:
        - Representa la distancia en línea recta sobre la esfera terrestre
        - Cualquier camino por carretera tendrá distancia >= geodésica
        
        Args:
            nodo: Identificador del nodo.
            
        Returns:
            Estimación del coste desde nodo hasta el destino.
        """
        return self.grafo.distancia_haversine(nodo, self.destino)
    
    def resolver(self):
        """
        Ejecuta el algoritmo A* para encontrar el camino óptimo.
        
        El algoritmo:
        1. Inicializa OPEN con el nodo origen
        2. Mientras OPEN no esté vacía:
           a. Extrae el nodo n con menor f(n)
           b. Si n es el objetivo, termina
           c. Añade n a CLOSED
           d. Para cada sucesor s de n:
              - Si s está en CLOSED, ignorar
              - Si s no está en OPEN, añadirlo
              - Si s está en OPEN con mayor g, actualizarlo
        
        Returns:
            Tupla (camino, coste) si encuentra solución, (None, None) si no.
        """
        # Inicializar OPEN con el nodo origen
        h_origen = self.heuristica(self.origen)
        self.abierta.insertar(self.origen, 0, h_origen)
        
        while not self.abierta.esta_vacia():
            # Extraer nodo con menor f(n)
            resultado = self.abierta.extraer_minimo()
            if resultado is None:
                break
            
            nodo_actual, g_actual = resultado
            
            # Verificar si ya está en cerrada (lazy deletion puede causar duplicados)
            if self.cerrada.contiene(nodo_actual):
                continue
            
            # Contar expansión
            self.expansiones += 1
            
            # Obtener padre y coste del arco (para el nodo origen no hay padre)
            # Necesitamos rastrear esto de otra forma
            # Modificamos para guardar el padre cuando insertamos en abierta
            
            # Comprobar si es el objetivo
            if nodo_actual == self.destino:
                self.coste_optimo = g_actual
                # Reconstruir camino
                camino = self.cerrada.reconstruir_camino(nodo_actual)
                return camino, g_actual
            
            # Expandir sucesores
            for sucesor, coste_arco in self.grafo.obtener_sucesores(nodo_actual):
                # Ignorar si ya está en CLOSED
                if self.cerrada.contiene(sucesor):
                    continue
                
                # Calcular nuevo g
                g_sucesor = g_actual + coste_arco
                
                # Calcular h
                h_sucesor = self.heuristica(sucesor)
                
                # Verificar si debemos añadir/actualizar en OPEN
                g_anterior = self.abierta.obtener_g(sucesor)
                
                if g_anterior is None or g_sucesor < g_anterior:
                    self.abierta.insertar(sucesor, g_sucesor, h_sucesor)
            
            # Añadir a CLOSED
            # Para el nodo origen, padre = None, coste_arco = 0
            if nodo_actual == self.origen:
                self.cerrada.insertar(nodo_actual, None, 0, g_actual)
            # Para otros nodos, necesitamos el padre
            # Modificamos la estructura para rastrear padres
        
        # No se encontró solución
        return None, None


class AlgoritmoAStarConPadres:
    """
    Implementación mejorada de A* que rastrea los padres correctamente.
    
    Esta versión mantiene un registro de qué nodo generó cada nodo
    para poder reconstruir el camino solución.
    """
    
    def __init__(self, grafo, origen, destino):
        """
        Inicializa el algoritmo A*.
        
        Args:
            grafo: Objeto Grafo con el problema.
            origen: Identificador del vértice de inicio.
            destino: Identificador del vértice objetivo.
        """
        self.grafo = grafo
        self.origen = origen
        self.destino = destino
        self.expansiones = 0
        self.coste_optimo = None
    
    def heuristica(self, nodo):
        """
        Calcula el valor heurístico h(n) usando distancia geodésica.
        
        Args:
            nodo: Identificador del nodo.
            
        Returns:
            Estimación admisible del coste hasta el destino.
        """
        return self.grafo.distancia_haversine(nodo, self.destino)
    
    def resolver(self):
        """
        Ejecuta A* con rastreo de padres para reconstrucción del camino.
        
        Returns:
            Tupla (camino, coste) donde camino es lista de (nodo, coste_arco).
        """
        import heapq
        
        # Estructuras de datos
        # OPEN: heap de (f, contador, nodo, g, padre, coste_arco_desde_padre)
        abierta = []
        contador = 0
        
        # Diccionario para valores g mínimos conocidos
        g_minimo = {self.origen: 0}
        
        # Diccionario para padres (nodo -> (padre, coste_arco))
        padres = {self.origen: (None, 0)}
        
        # CLOSED: conjunto de nodos expandidos
        cerrada = set()
        
        # Insertar nodo origen
        h_origen = self.heuristica(self.origen)
        heapq.heappush(abierta, (h_origen, contador, self.origen, 0))
        
        while abierta:
            f, _, nodo_actual, g_actual = heapq.heappop(abierta)
            
            # Si ya está en cerrada, ignorar (lazy deletion)
            if nodo_actual in cerrada:
                continue
            
            # Si el g actual es peor que el conocido, ignorar
            if g_actual > g_minimo.get(nodo_actual, float('inf')):
                continue
            
            # Contar expansión
            self.expansiones += 1
            
            # Añadir a cerrada
            cerrada.add(nodo_actual)
            
            # Comprobar si es el objetivo
            if nodo_actual == self.destino:
                self.coste_optimo = g_actual
                # Reconstruir camino
                camino = self._reconstruir_camino(padres, nodo_actual)
                return camino, g_actual
            
            # Expandir sucesores
            for sucesor, coste_arco in self.grafo.obtener_sucesores(nodo_actual):
                # Ignorar si ya está en cerrada
                if sucesor in cerrada:
                    continue
                
                # Calcular nuevo g
                g_sucesor = g_actual + coste_arco
                
                # Si encontramos un mejor camino
                if g_sucesor < g_minimo.get(sucesor, float('inf')):
                    g_minimo[sucesor] = g_sucesor
                    padres[sucesor] = (nodo_actual, coste_arco)
                    
                    h_sucesor = self.heuristica(sucesor)
                    f_sucesor = g_sucesor + h_sucesor
                    
                    contador += 1
                    heapq.heappush(abierta, (f_sucesor, contador, sucesor, g_sucesor))
        
        # No se encontró solución
        return None, None
    
    def _reconstruir_camino(self, padres, nodo_objetivo):
        """
        Reconstruye el camino desde el origen hasta el objetivo.
        
        Args:
            padres: Diccionario {nodo: (padre, coste_arco)}.
            nodo_objetivo: Nodo final del camino.
            
        Returns:
            Lista de tuplas (nodo, coste_arco).
        """
        camino = []
        nodo_actual = nodo_objetivo
        
        while nodo_actual is not None:
            padre, coste_arco = padres[nodo_actual]
            camino.append((nodo_actual, coste_arco))
            nodo_actual = padre
        
        camino.reverse()
        return camino


class AlgoritmoDijkstra:
    """
    Implementación del algoritmo de Dijkstra (A* con h(n) = 0).
    
    Dijkstra es un algoritmo de fuerza bruta que garantiza encontrar
    la solución óptima pero sin usar información heurística.
    Se utiliza como baseline para comparar con A*.
    
    La diferencia con A*:
    - Dijkstra: f(n) = g(n)
    - A*: f(n) = g(n) + h(n)
    
    Por tanto, Dijkstra expande más nodos que A* con buena heurística.
    """
    
    def __init__(self, grafo, origen, destino):
        """
        Inicializa el algoritmo de Dijkstra.
        
        Args:
            grafo: Objeto Grafo con el problema.
            origen: Identificador del vértice de inicio.
            destino: Identificador del vértice objetivo.
        """
        self.grafo = grafo
        self.origen = origen
        self.destino = destino
        self.expansiones = 0
        self.coste_optimo = None
    
    def resolver(self):
        """
        Ejecuta Dijkstra para encontrar el camino más corto.
        
        Returns:
            Tupla (camino, coste) donde camino es lista de (nodo, coste_arco).
        """
        import heapq
        
        # OPEN: heap de (g, contador, nodo)
        abierta = []
        contador = 0
        
        # Diccionario para valores g mínimos conocidos
        g_minimo = {self.origen: 0}
        
        # Diccionario para padres
        padres = {self.origen: (None, 0)}
        
        # CLOSED
        cerrada = set()
        
        # Insertar nodo origen
        heapq.heappush(abierta, (0, contador, self.origen))
        
        while abierta:
            g_actual, _, nodo_actual = heapq.heappop(abierta)
            
            if nodo_actual in cerrada:
                continue
            
            if g_actual > g_minimo.get(nodo_actual, float('inf')):
                continue
            
            self.expansiones += 1
            cerrada.add(nodo_actual)
            
            if nodo_actual == self.destino:
                self.coste_optimo = g_actual
                camino = self._reconstruir_camino(padres, nodo_actual)
                return camino, g_actual
            
            for sucesor, coste_arco in self.grafo.obtener_sucesores(nodo_actual):
                if sucesor in cerrada:
                    continue
                
                g_sucesor = g_actual + coste_arco
                
                if g_sucesor < g_minimo.get(sucesor, float('inf')):
                    g_minimo[sucesor] = g_sucesor
                    padres[sucesor] = (nodo_actual, coste_arco)
                    contador += 1
                    heapq.heappush(abierta, (g_sucesor, contador, sucesor))
        
        return None, None
    
    def _reconstruir_camino(self, padres, nodo_objetivo):
        """Reconstruye el camino desde origen hasta objetivo."""
        camino = []
        nodo_actual = nodo_objetivo
        
        while nodo_actual is not None:
            padre, coste_arco = padres[nodo_actual]
            camino.append((nodo_actual, coste_arco))
            nodo_actual = padre
        
        camino.reverse()
        return camino