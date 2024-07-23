import json
from flask import Flask, request, redirect

app = Flask(__name__)

recetas_file = 'recetas.json'

try:
    with open(recetas_file, 'r') as f:
        recetas = json.load(f)
except FileNotFoundError:
    recetas = []

def guardar_recetas():
    with open(recetas_file, 'w') as f:
        json.dump(recetas, f, indent=4)

@app.route('/')
def index():
    return '''
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Inicio</title>
    </head>
    <body>
        <h1>Bienvenido</h1>
        <a href="/recetas">Ver recetas</a>
    </body>
    </html>
    '''

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_receta():
    if request.method == 'POST':
        nombre = request.form['nombre']
        ingredientes = request.form['ingredientes']
        pasos = request.form['pasos']
        receta = {
            "id": str(len(recetas) + 1),
            "nombre": nombre,
            "ingredientes": ingredientes.split(', '),
            "pasos": pasos.split('. ')
        }
        recetas.append(receta)
        guardar_recetas()
        return redirect('/recetas')
    
    return '''
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Agregar Receta</title>
    </head>
    <body>
        <h1>Agregar Receta</h1>
        <form action="/agregar" method="POST">
            <label for="nombre">Nombre:</label>
            <input type="text" id="nombre" name="nombre" required><br>
            <label for="ingredientes">Ingredientes (separados por coma):</label>
            <input type="text" id="ingredientes" name="ingredientes" required><br>
            <label for="pasos">Pasos (separados por punto):</label>
            <textarea id="pasos" name="pasos" required></textarea><br>
            <button type="submit">Agregar</button>
        </form>
    </body>
    </html>
    '''

@app.route('/eliminar/<string:id_receta>', methods=['POST'])
def eliminar_receta(id_receta):
    global recetas
    recetas = [receta for receta in recetas if receta['id'] != id_receta]
    guardar_recetas()
    return redirect('/recetas')

@app.route('/recetas')
def ver_listado():
    listado = '''
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Listado de Recetas</title>
    </head>
    <body>
        <h1>Listado de Recetas</h1>
        <ul>
    '''
    for receta in recetas:
        listado += f'''
        <li>{receta["nombre"]} - 
            <a href="/receta/{receta["id"]}">Ver</a> - 
            <form action="/eliminar/{receta["id"]}" method="POST">
                <button type="submit">Eliminar</button>
            </form>
        </li>
        '''
    listado += '''
        </ul>
        <a href="/agregar">Agregar Receta</a>
    </body>
    </html>
    '''
    return listado

@app.route('/receta/<string:id_receta>')
def ver_receta(id_receta):
    receta = next((receta for receta in recetas if receta['id'] == id_receta), None)
    if receta:
        detalles = '''
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Detalles de la Receta</title>
        </head>
        <body>
            <h1>Detalles de la Receta</h1>
            <p>Nombre: {nombre}</p>
            <p>Ingredientes: {ingredientes}</p>
            <p>Pasos: {pasos}</p>
            <form action="/eliminar/{id_receta}" method="POST"><button type="submit">Eliminar</button></form>
        </body>
        </html>
        '''.format(nombre=receta['nombre'], ingredientes=', '.join(receta['ingredientes']), pasos='. '.join(receta['pasos']), id_receta=receta['id'])
        return detalles
    return "Receta no encontrada."

if __name__ == '__main__':
    app.run(debug=True)





