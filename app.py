import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
aprendices = db[os.getenv("COLLECTION_NAME")]


# 10.1. Consultar la cantidad de aprendices
@app.route("/api/cantidadAprendices", methods=["GET"])
def cantidad_aprendices():
    cantidad = aprendices.count_documents({})
    return jsonify({"CantidadAprendices": cantidad})


# 10.2. Cantidad de aprendices por nivel de formación
@app.route("/api/cantidadAprendices/<nivel>", methods=["GET"])
def cantidad_aprendices_nivel(nivel):
    cantidad = aprendices.count_documents({"NIVEL_DE_FORMACION": nivel})
    return jsonify({"Nivel": nivel, "CantidadAprendices": cantidad})

# 10.3. Listado de programas por nivel de formación (sin duplicados)
@app.route("/api/programas/<nivel>", methods=["GET"])
def programas_por_nivel(nivel):
    programas = aprendices.distinct("PROGRAMA", {"NIVEL_DE_FORMACION": nivel})
    return jsonify({
        "Nivel": nivel,
        "TotalProgramas": len(programas),
        "Programas": programas
    })

# 10.4. Listado de todos los programas de formación (sin duplicados)
@app.route("/api/programas", methods=["GET"])
def todos_los_programas():
    programas = aprendices.distinct("PROGRAMA")
    return jsonify({
        "TotalProgramas": len(programas),
        "Programas": programas
    })

    # 10.5. Cantidad de aprendices por programa de formación
@app.route("/api/cantidadAprendicesPrograma/<programa>", methods=["GET"])
def cantidad_aprendices_programa(programa):
    cantidad = aprendices.count_documents({"PROGRAMA": programa})
    return jsonify({
        "Programa": programa,
        "CantidadAprendices": cantidad
    })

  # 10.6. Aprendices de un programa con estado de ficha "Terminada por unificación"
@app.route("/api/terminadaUnificacion/<programa>", methods=["GET"])
def terminada_unificacion(programa):
    estado = "Terminada por unificación"
    consulta = {
        "PROGRAMA": programa,
        "ESTADO_FICHA": estado
    }
    proyeccion = {
        "_id": 0,
        "FICHA": 1,
        "NUMERO_DOCUMENTO": 1,
        "NOMBRE": 1,
        "PRIMER_APELLIDO": 1,
        "SEGUNDO_APELLIDO": 1
    }
    lista_aprendices = list(aprendices.find(consulta, proyeccion))
    return jsonify({
        "Programa": programa,
        "Estado de la ficha": estado,
        "Aprendices": lista_aprendices
    })

    # 10.7. Aprendices de un programa de formación específico
@app.route("/api/aprendicesPrograma/<programa>", methods=["GET"])
def aprendices_por_programa(programa):
    consulta = {"PROGRAMA": programa}
    proyeccion = {
        "_id": 0,
        "FICHA": 1,
        "NUMERO_DOCUMENTO": 1,
        "NOMBRE": 1,
        "PRIMER_APELLIDO": 1,
        "SEGUNDO_APELLIDO": 1,
        "ESTADO_APRENDIZ": 1
    }
    lista_aprendices = list(aprendices.find(consulta, proyeccion))
    return jsonify({
        "Programa": programa,
        "TotalAprendices": len(lista_aprendices),
        "Aprendices": lista_aprendices
    })

    # 10.8. Cantidad de aprendices certificados por programa de formación
@app.route("/api/cantidadCertificados/<programa>", methods=["GET"])
def cantidad_certificados(programa):
    cantidad = aprendices.count_documents({
        "PROGRAMA": programa,
        "ESTADO_APRENDIZ": "Certificado"
    })
    return jsonify({
        "Programa": programa,
        "Estado": "Certificado",
        "CantidadCertificados": cantidad
    })

    # 10.9. Aprendices de una ficha según su estado de aprendiz
@app.route("/api/porEstado/<ficha>/<estado>", methods=["GET"])
def por_estado(ficha, estado):
    ficha_valor = int(ficha) if ficha.isdigit() else ficha
    consulta = {
        "FICHA": ficha_valor,
        "ESTADO_APRENDIZ": estado
    }
    proyeccion = {
        "_id": 0,
        "FICHA": 1,
        "NUMERO_DOCUMENTO": 1,
        "NOMBRE": 1,
        "PRIMER_APELLIDO": 1,
        "SEGUNDO_APELLIDO": 1,
        "ESTADO_APRENDIZ": 1
    }
    lista_aprendices = list(aprendices.find(consulta, proyeccion))
    return jsonify({
        "Ficha": ficha_valor,
        "Estado": estado,
        "TotalAprendices": len(lista_aprendices),
        "Aprendices": lista_aprendices
    })

    # 10.10. Programas de formación complementaria / virtual (sin duplicados)
@app.route("/api/programasComplementariaVirtual", methods=["GET"])
def programas_complementaria_virtual():
    filtro = {
        "PROGRAMA": {
            "$regex": "COMPLEMENTAR|VIRTUAL",
            "$options": "i"
        }
    }
    programas = aprendices.distinct("PROGRAMA", filtro)
    return jsonify({
        "TotalProgramas": len(programas),
        "Programas": programas
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)