import hashlib
import sqlite3
from flask import Flask, request, jsonify

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos SQLite
conn = sqlite3.connect('usuarios.db', check_same_thread=False)
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 nombre TEXT NOT NULL,
                 hash_password TEXT NOT NULL)''')
conn.commit()

# Función para registrar usuarios
def registrar_usuario(nombre, password):
    hash_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("INSERT INTO usuarios (nombre, hash_password) VALUES (?, ?)",
                   (nombre, hash_password))
    conn.commit()

# Registrar los tres usuarios al iniciar el script
usuarios = [
    ("jose cannobbio", "cisco1"),
    ("sebastian morales", "cisco2"),
    ("julio mancilla", "cisco3")
]

for usuario in usuarios:
    registrar_usuario(usuario[0], usuario[1])

# Rutas de la aplicación Flask

# Ruta para registrar usuarios y guardar sus contraseñas hasheadas
@app.route('/registrar', methods=['POST'])
def registrar_usuario_api():
    data = request.get_json()
    nombre = data['nombre']
    password = data['password']
    
    # Generar hash de la contraseña
    hash_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Insertar usuario y contraseña hasheada en la base de datos
    cursor.execute("INSERT INTO usuarios (nombre, hash_password) VALUES (?, ?)",
                   (nombre, hash_password))
    conn.commit()
    
    return jsonify({"mensaje": "Usuario registrado correctamente"})

# Ruta para validar usuarios
@app.route('/validar', methods=['POST'])
def validar_usuario():
    data = request.get_json()
    nombre = data['nombre']
    password = data['password']
    
    # Obtener hash almacenado en la base de datos para el usuario dado
    cursor.execute("SELECT hash_password FROM usuarios WHERE nombre=?", (nombre,))
    result = cursor.fetchone()
    
    if result:
        hash_password = result[0]
        # Comparar la contraseña ingresada con el hash almacenado
        if hashlib.sha256(password.encode()).hexdigest() == hash_password:
            return jsonify({"mensaje": "Usuario validado correctamente"})
    
    return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

# Iniciar la aplicación Flask en el puerto 5800
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5800)