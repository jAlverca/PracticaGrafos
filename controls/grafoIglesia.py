import json
import math
import os

from controls.iglesiaDaoControl import IglesiaDaoControl
from controls.tda.grafo.graph_label_no_managed import GraphLabelNoManaged
from controls.tda.list.linked_list import Linked_List


def construct_graph_data(grafo):
    """Construye un diccionario representando el grafo para serialización."""
    vertices = grafo.num_vertex
    aristas = grafo.num_edges
    adyacencias = []
    registradas = Linked_List()
    for origen in range(vertices):
        for arista in grafo.adjacent(origen):
            destino = arista._destination
            peso = arista._weight
            clave = min(origen, destino), max(origen, destino)
            if clave not in registradas.to_array:
                adyacencias.append({"origen": origen, "destino": destino, "peso": peso})
                registradas.add_last(clave)
    return {"vertices": vertices, "aristas": aristas, "adyacencias": adyacencias}


def load_graph_data(grafo, iglesias, data):
    """Carga los datos del grafo desde un diccionario."""
    for vertice in range(data["vertices"]):
        grafo.label_vertex(vertice, iglesias.to_array[vertice])
    for arista in data["adyacencias"]:
        origen = iglesias.busquedaBinaria("_id", arista["origen"])
        destino = iglesias.busquedaBinaria("_id", arista["destino"])
        peso = arista["peso"]
        grafo.insert_edge_w_label(origen, destino, peso)


def calcular_distancia(lat1, lon1, lat2, lon2):
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)

    rad = math.pi / 180
    earth_radius_km = 6378.137

    dlat = (lat2 - lat1) * rad
    dlon = (lon2 - lon1) * rad

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1 * rad) * math.cos(lat2 * rad) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance_km = earth_radius_km * c

    return round(distance_km, 3)


class GrafoIglesia:
    def __init__(self):
        self._grafo = None
        self._iglesia_control_dao = IglesiaDaoControl()
        self._ruta_archivo = os.path.join(
            os.path.dirname(__file__), "../data", "GrafoIglesia.json"
        )

    def existe_archivo(self):
        return os.path.isfile(self._ruta_archivo)

    def guardar_grafo(self):
        datos = construct_graph_data(self._grafo)
        with open(self._ruta_archivo, "w") as archivo:
            json.dump(datos, archivo, indent=4)

    def cargar_grafo(self):
        if self.existe_archivo():
            try:
                iglesias = self._iglesia_control_dao.list()
                with open(self._ruta_archivo, "r") as archivo:
                    datos = json.load(archivo)
                self._grafo = GraphLabelNoManaged(iglesias._length)
                load_graph_data(self._grafo, iglesias, datos)
            except Exception as e:
                print(e)
        else:
            print("No existe el archivo")
            self.crear_grafo()

    def crear_grafo(self):
        iglesias = self._iglesia_control_dao.list()
        if iglesias:
            self._grafo = GraphLabelNoManaged(iglesias._length)
            for vertice, parada in enumerate(iglesias.to_array):
                self._grafo.label_vertex(vertice, parada)
            self.guardar_grafo()

    def insertar_arista(self, origen, destino, peso):
        self._grafo.insert_edge_w_label(origen, destino, peso)

    def obtener_matriz_adyacencia(self):
        vertices = self._grafo.num_vertex
        matriz = [[0] * vertices for _ in range(vertices)]
        for origen in range(vertices):
            for arista in self._grafo.adjacent(origen):
                destino = arista._destination
                peso = arista._weight
                matriz[origen][destino] = peso
        return matriz

    def camino_dijkstra(self, origen, destino):
        return self._grafo.camino_dijkstra(origen, destino)

    def camino_floyd(self):
        return self._grafo.camino_floyd()
