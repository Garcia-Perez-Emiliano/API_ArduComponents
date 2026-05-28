import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv 

# Cargar las variables de entorno
load_dotenv()

# Crear instancia
app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de la base de datos para ArduComponents
class Componente(db.Model):
    __tablename__ = 'componentes'
    id_componente = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    categoria = db.Column(db.String) # Ej: 'Microcontrolador', 'Sensor', 'Herramienta'
    stock = db.Column(db.Integer, default=0)
    precio = db.Column(db.Float)

# Endpoint para obtener todos los componentes
@app.route('/', methods=['GET'])
def get_componentes():
    componentes = Componente.query.all()
    lista_componentes = []
    for comp in componentes:
        lista_componentes.append({
            'id_componente': comp.id_componente,
            'nombre': comp.nombre,
            'categoria': comp.categoria,
            'stock': comp.stock,
            'precio': comp.precio
        })
    return jsonify(lista_componentes)
    
# Endpoint para obtener un componente específico por su id
@app.route('/<id_componente>', methods=['GET'])
def get_componente(id_componente):
    comp = Componente.query.get(id_componente)
    if comp is None:
        return jsonify({'msj':'Componente no encontrado'}), 404
        
    return jsonify({
        'id_componente': comp.id_componente,
        'nombre': comp.nombre,
        'categoria': comp.categoria,
        'stock': comp.stock,
        'precio': comp.precio,
    })

# Endpoint para eliminar un componente
@app.route('/<id_componente>', methods=['DELETE'])
def delete_componente(id_componente):
    comp = Componente.query.get(id_componente)
    if comp is None:
        return jsonify({'msj':'Componente no encontrado'}), 404
        
    db.session.delete(comp)
    db.session.commit()
    return jsonify({'msj':'Componente eliminado correctamente'})

# Endpoint para agregar un nuevo componente
@app.route('/', methods=['POST'])
def insert_componente():
    data = request.get_json()
    nuevo_componente = Componente(
        id_componente = data['id_componente'],
        nombre = data['nombre'],
        categoria = data.get('categoria', 'General'),
        stock = data.get('stock', 0),
        precio = data['precio']
    )
    db.session.add(nuevo_componente)
    db.session.commit()
    return jsonify({'msj':'Componente agregado correctamente'}), 201

# Endpoint para actualizar un componente existente
@app.route('/<id_componente>', methods=['PUT'])
def update_componente(id_componente):
    comp = Componente.query.get(id_componente)
    if comp is None:
        return jsonify({'msg': 'Componente no encontrado'}), 404

    data = request.get_json()

    if "nombre" in data:
        comp.nombre = data['nombre']
    if "categoria" in data:
        comp.categoria = data['categoria']
    if "stock" in data:
        comp.stock = data['stock']
    if "precio" in data:
        comp.precio = data['precio']

    db.session.commit()
    return jsonify({'msg': 'Componente actualizado correctamente'})

# Creación de tablas automáticamente en caso de que no existan
with app.app_context():
    db.create_all()  

if __name__ == '__main__':
    app.run(debug=True)