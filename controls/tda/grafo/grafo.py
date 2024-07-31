import heapq
import os
import time


class Graph:
    @property
    def num_vertex(self):
        raise NotImplementedError("Please Implement this method")

    @property
    def num_edges(self):
        raise NotImplementedError("Please Implement this method")

    def exist_edge(self, u, v):
        raise NotImplementedError("Please Implement this method")

    def weight_edge(self, u, v):
        raise NotImplementedError("Please Implement this method")

    def insert_edge(self, u, v):
        raise NotImplementedError("Please Implement this method")

    def insert_edge_w(self, u, v, weight):
        raise NotImplementedError("Please Implement this method")

    def adjacent(self, u):
        raise NotImplementedError("Please Implement this method")

    def __str__(self) -> str:
        out = ""
        for i in range(self.num_vertex):
            out += f"Vertex {str(i)}: \n"
            adjs = self.adjacent(i)
            for j in range(adjs._length):
                out += f"\t{adjs.to_array[j]}\n"
        return out

    def print_graph(self):
        # Ruta del archivo .js que se generará.
        path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../../static")
        )
        path = os.path.join(path, r"d3\grafo.js")

        data = ""
        # Definición de nodos en el archivo .js
        data += "var nodes = ([\n"
        for i in range(self.num_vertex):
            label = self.get_label(i) if self.get_label(i) is not None else i
            data += f"  {{id: {i}, label: '{label}'}},\n"
        data += "]);\n\n"

        # Definición de aristas en el archivo .js
        data += "var edges = ([\n"
        for i in range(self.num_vertex):
            adjs = self.adjacent(i)
            for j in range(adjs._length):
                dest_label = (
                    self.get_label(adjs.to_array[j]._destination)
                    if self.get_label(adjs.to_array[j]._destination) is not None
                    else adjs.to_array[j]._destination
                )
                data += f"  {{from: {i}, to: {adjs.to_array[j]._destination}, label: '{adjs.to_array[j]._weight}'}},\n"
        data += "]);\n\n"

        # Generación del código JavaScript para visualización
        js = ""
        js += "var data = {\n"
        js += "  nodes: nodes,\n"
        js += "  edges: edges,\n"
        js += "};\n"
        js += "var container = document.getElementById('mynetwork');\n"
        js += "var options = {};\n"
        js += "var network = new vis.Network(container, data, options);\n"

        # Escritura en el archivo
        try:
            with open(path, "w") as file:
                file.write(data)
                file.write(js)
        except Exception as e:
            print(e)

    def __repr__(self):
        return self.__str__()

    __doc__ = __str__

    def camino_dijkstra(self, origen, destino) -> list:
        star = time.time()
        num_vertices = self.num_vertex
        distancias = [float("inf")] * num_vertices
        predecesores = [None] * num_vertices
        visitados = [False] * num_vertices
        distancias[origen] = 0

        cola_prioridad = [(0, origen)]

        while cola_prioridad:
            distancia_actual, u = heapq.heappop(cola_prioridad)

            if visitados[u]:
                continue

            visitados[u] = True

            for v in range(num_vertices):
                if self.exist_edge(u, v):
                    distancia_alternativa = distancias[u] + self.weight_edge(u, v)
                    if distancia_alternativa < distancias[v]:
                        distancias[v] = distancia_alternativa
                        predecesores[v] = u
                        heapq.heappush(cola_prioridad, (distancia_alternativa, v))
        end = time.time()
        print(f"Tiempo de ejecución: {end - star:.10f}")
        camino_mas_corto = []
        paso = destino
        while paso is not None:
            camino_mas_corto.insert(0, paso)
            paso = predecesores[paso]

        if distancias[destino] == float("inf"):
            return []

        return camino_mas_corto

    def camino_floyd(self):
        star1 = time.time()
        num_vertices = self.num_vertex
        matriz_distancias = [[float("inf")] * num_vertices for _ in range(num_vertices)]
        matriz_siguientes = [[None] * num_vertices for _ in range(num_vertices)]

        for i in range(num_vertices):
            matriz_distancias[i][i] = 0

        for i in range(num_vertices):
            for j in range(num_vertices):
                if self.exist_edge(i, j):
                    matriz_distancias[i][j] = self.weight_edge(i, j)
                    matriz_siguientes[i][j] = j

        for k in range(num_vertices):
            for i in range(num_vertices):
                for j in range(num_vertices):
                    if matriz_distancias[i][k] < float("inf") and matriz_distancias[k][
                        j
                    ] < float("inf"):
                        if (
                            matriz_distancias[i][k] + matriz_distancias[k][j]
                            < matriz_distancias[i][j]
                        ):
                            matriz_distancias[i][j] = (
                                matriz_distancias[i][k] + matriz_distancias[k][j]
                            )
                            matriz_siguientes[i][j] = matriz_siguientes[i][k]
        end1 = time.time()
        print(f"Tiempo de ejecución: {end1 - star1}")

        return matriz_distancias, matriz_siguientes
