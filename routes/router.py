from flask import Blueprint, request, redirect, render_template, url_for, jsonify

from controls.grafoIglesia import GrafoIglesia
from controls.iglesiaDaoControl import IglesiaDaoControl


router = Blueprint("router", __name__)

ic = IglesiaDaoControl()
gi = GrafoIglesia()
@router.route("/grafo")
def grafo():
    iglesias = ic.list()
    print(iglesias)
    return render_template("grafo.html", iglesias=iglesias)


@router.route("/grafo_iglesia")
def grafo_iglesia():
    iglesias = ic.list()
    return render_template("grafo.html", iglesias=iglesias)


@router.route("/grafo_admin")
def grafo_admin():
    iglesias = ic.list()
    return render_template("iglesia/grafo_admin.html", iglesias=iglesias)


@router.route("/")
def listar_iglesias():
    iglesias = ic.list()
    return render_template("iglesia/lista.html", iglesias=iglesias)


@router.route("/grafo_admin_matriz", methods=["GET"])
def guardar_adyacencia():
    id_origen = request.args.get("origen")
    id_destino = request.args.get("destino")

    if id_origen == id_destino:
        return jsonify({"error": "Debe seleccionar un negocio diferente"})

    gi = GrafoIglesia()
    gi.cargar_grafo()
    ic = IglesiaDaoControl()
    iglesias = ic.list()
    origen = iglesias.busquedaBinaria("_id", int(id_origen))
    destino = iglesias.busquedaBinaria("_id", int(id_destino))

    if not origen or not destino:
        return jsonify({"error": "Iglesia no encontrada"})

    gi.insertar_arista(
        origen,
        destino,
        ic.calcular_distancia(
            origen._latitud, origen._longitud, destino._latitud, destino._longitud
        ),
    )

    gi.guardar_grafo()

    matriz = gi.obtener_matriz_adyacencia()

    return jsonify(
        {
            "success": "Adyacencia guardada correctamente",
            "matriz": matriz,
            "negocios": [n._nombre for n in iglesias],
        }
    )


@router.route("/matriz", methods=["GET"])
def cargar_adyacencia():
    try:
        print(1)
        gi.cargar_grafo()
        print(2)
        matriz = gi.obtener_matriz_adyacencia()
        print(3)
        negocios = ic.list()
        print(4)
        return jsonify({"matriz": matriz, "negocios": [n._nombre for n in negocios]})
    except Exception as e:
        print(e)
        return jsonify({"error": "No se pudo cargar la adyacencia"})


@router.route("/iglesia/nuevo", methods=["GET", "POST"])
def nuevo_iglesia():
    if request.method == "POST":
        data = request.form
        ic._iglesia._nombre = data["nombre"]
        ic._iglesia._direccion = data["direccion"]
        ic._iglesia._longitud = data["longitud"]
        ic._iglesia._latitud = data["latitud"]
        ic.save
        return redirect(url_for("router.listar_iglesias"))
    return render_template("iglesia/guardar.html")


@router.route("/buscar", methods=["GET"])
def buscar_iglesia():
    id_origen = request.args.get("origen")
    id_destino = request.args.get("destino")
    tipoBusqueda = request.args.get("tipo_busqueda")

    # Validar los parámetros
    if not id_origen or not id_destino or not tipoBusqueda:
        return jsonify({"error": "Faltan parámetros en la solicitud"}), 400

    try:
        iglesias = ic.list()
        origen = iglesias.busquedaBinaria("_id", int(id_origen))
        destino = iglesias.busquedaBinaria("_id", int(id_destino))
        print(origen, destino)
        print(tipoBusqueda)

        gi.cargar_grafo()
        if tipoBusqueda == "1":
            print("Dijkstra")
            resultado = gi.camino_dijkstra(int(id_origen), int(id_destino))

            print(resultado)
            camino_objetos = [
                iglesias.busquedaBinaria("_id", id).serializable() for id in resultado
            ]
            response = {"camino": camino_objetos}

            return jsonify(response)

        else:
            matriz_distancias, matriz_siguientes = gi.camino_floyd()
            camino = reconstruir_camino(
                matriz_siguientes, int(id_origen), int(id_destino)
            )
            camino_objetos = [
                iglesias.busquedaBinaria("_id", id).serializable() for id in camino
            ]
            response = {"camino": camino_objetos}

        return jsonify(response)

    except Exception as e:
        print(e)
        return jsonify({"error": "No se pudo procesar la solicitud"}), 500


def reconstruir_camino(matriz_siguientes, origen, destino):
    if matriz_siguientes[origen][destino] is None:
        return []

    camino = [origen]
    while origen != destino:
        origen = matriz_siguientes[origen][destino]
        camino.append(origen)

    return camino
