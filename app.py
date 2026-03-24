from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('examen.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()

    fecha = request.args.get('fecha')

    restaurante = conn.execute('SELECT * FROM restaurante').fetchone()

    if fecha:
        menu = conn.execute(
            'SELECT * FROM menu_almuerzo WHERE fecha = ?',
            (fecha,)
        ).fetchall()
    else:
        menu = []

    # 🔥 convertir a diccionario y limpiar espacios
    restaurante = dict(restaurante)
    restaurante['imagen_portada'] = restaurante['imagen_portada'].strip()

    menu = [dict(row) for row in menu]
    for plato in menu:
        plato['imagen'] = plato['imagen'].strip()

    conn.close()

    return render_template(
        'index.html',
        restaurante=restaurante,
        menu=menu,
        fecha=fecha
    )

if __name__ == '__main__':
    app.run(debug=True)