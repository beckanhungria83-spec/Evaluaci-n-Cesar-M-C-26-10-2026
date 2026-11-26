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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)