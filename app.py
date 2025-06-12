from flask import Flask, request, jsonify
from flask_cors import CORS
from peewee import *
import os

from playhouse.db_url import connect

DATABASE_URL = "postgresql://todo_db_bzu7_user:TdzPBhOzzpytTjwtEkKjrm2TqQNazWV2@dpg-d14uj86mcj7s738ddb80-a.oregon-postgres.render.com:5432/todo_db_bzu7"
db = connect(DATABASE_URL)

# Definición del modelo
class BaseModel(Model):
    class Meta:
        database = db

class Tarea(BaseModel):
    titulo = CharField()
    descripcion = TextField(null=True)
    completado = BooleanField(default=False)

# Crear las tablas si no existen
db.connect()
db.create_tables([Tarea])

# Inicializar Flask
app = Flask(__name__)
CORS(app)

@app.route("/")
def health_check():
    return {"status": "ok", "message": "API corriendo"}

# Rutas CRUD
@app.route('/tareas', methods=['POST'])
def crear_tarea():
    data = request.get_json()
    tarea = Tarea.create(
        titulo=data['titulo'],
        descripcion=data.get('descripcion'),
        completado=data.get('completado', False)
    )
    return jsonify(modelo_a_diccionario(tarea)), 201

@app.route('/tareas', methods=['GET'])
def obtener_tareas():
    tareas = Tarea.select()
    return jsonify([modelo_a_diccionario(t) for t in tareas])

@app.route('/tareas/<int:id>', methods=['GET'])
def obtener_tarea(id):
    try:
        tarea = Tarea.get(Tarea.id == id)
        return jsonify(modelo_a_diccionario(tarea))
    except Tarea.DoesNotExist:
        return jsonify({"error": "Tarea no encontrada"}), 404

@app.route('/tareas/<int:id>', methods=['PUT'])
def actualizar_tarea(id):
    try:
        tarea = Tarea.get(Tarea.id == id)
        data = request.get_json()
        tarea.titulo = data.get('titulo', tarea.titulo)
        tarea.descripcion = data.get('descripcion', tarea.descripcion)
        tarea.completado = data.get('completado', tarea.completado)
        tarea.save()
        return jsonify(modelo_a_diccionario(tarea))
    except Tarea.DoesNotExist:
        return jsonify({"error": "Tarea no encontrada"}), 404

@app.route('/tareas/<int:id>', methods=['DELETE'])
def eliminar_tarea(id):
    try:
        tarea = Tarea.get(Tarea.id == id)
        tarea.delete_instance()
        return jsonify({"mensaje": "Tarea eliminada correctamente"})
    except Tarea.DoesNotExist:
        return jsonify({"error": "Tarea no encontrada"}), 404

# Función auxiliar
def modelo_a_diccionario(tarea):
    return {
        "id": tarea.id,
        "titulo": tarea.titulo,
        "descripcion": tarea.descripcion,
        "completado": tarea.completado
    }

# Punto de entrada
if __name__ == '__main__':
    app.run(debug=True)