from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'adoptaF'

conexion = MySQL(app)


@app.before_request
def before_request():
    print("antes de la petición...")


@app.after_request
def after_request(response):
    print("Después de la petición")
    return response


@app.route('/')
def index():
    # return "<h1>Tronsky</h1>"

    # lista de perritos
    lista_perritos = [
        'Perrito 1', 'Perrito 2', 'Perrito 3', 'Perrito 4', 'Perrito 5', 'Perrito 6']

    # diccionario data
    data = {
        'titulo': 'Adopta Fácil',
        'bienvenida': '¡Adoptar es más fácil!',
        'lista_perritos': lista_perritos,
        'numero_perritos': len(lista_perritos)
    }
    return render_template('index.html', data=data)


@app.route('/contacto/<nombre>')
def contacto(nombre,):
    data = {
        'titulo': 'Contacto',
        'nombre': nombre
    }
    return render_template('contacto.html', data=data)


def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    print(request.args.get('param2'))
    return "Ok"


@app.route('/en_adopcion')
def listar_perritos():
    data = {}
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT codigo, nombre, edad, contacto, nombre_contacto, FROM perritos ORDER BY codigo ASC"
        cursor.execute(sql)
        perritos = cursor.fetchall()
        # print(perritos)
        data['perritos'] = perritos
        data['mensaje'] = 'Exito'
        return jsonify(data)
    except Exception as ex:
        data['mensaje'] = 'Error...'


def pagina_no_encontrada(error):
    return render_template('404.html'), 404
    # return redirect(url_for('index'))


if __name__ == '__main__':
    app.add_url_rule('/query_string', view_func=query_string)
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=50)
