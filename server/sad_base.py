#!/usr/bin/python
# -*- coding: utf-8 -*-

# descomentar para usar en PythonAnywhere
# from bottle import default_app

from bottle import route, request, template, static_file, run

import datetime

# líneas en el listado
MAX_LINEAS = 20


@route('/datain')
def guardar_datos():
    """
        recibe y guarda los datos
    """
    # obtiene temperatura, humedad, sensor del request 
    temp = request.query.tempe
    hume = request.query.hume

    sens_nro = request.query.snum

    # si no hay sensor, le asigna 0
    if sens_nro == "":
        sens_nro = "0"

    # fecha y hora actual en formato YYYY-MM-DD, HH:MM:SS
    tstamp = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")

    # ip de origen 
    ip_orig = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')

    # guarda los datos recibidos en un archivo de texto
    try:
        f = open("datos.csv", "a")
        linea_datos = temp + ";" + hume + ";" + sens_nro + ";" + tstamp + ";" + ip_orig + "\n"
        f.write(linea_datos)
        f.close()
    except Exception as e:
        print(e)


@route('/')
def index():
    return template('templates/index.html')


@route('/listado')
def listado_datos():
    """
        lee MAX_LINEAS del archivo
        y los envía en una lista
    """
    mediciones = []

    try:
        with open('datos.csv') as f:
            mediciones = list(f)[:-MAX_LINEAS - 1:-1]
    except:
        mediciones = ['?;?;?;?;?']

    # print(mediciones)

    return template('templates/lista.html', 
                        datos=mediciones,
                        list_sep=';')


@route('/contacto')
def contacto():
	return "contacto"


@route('/<filepath:path>')
def server_static(filepath):    
    """ necesario para archivos estáticos (.css, imagenes, etc.) """
    return static_file(filepath, root='.')


# ejecuta server de desarrollo
run(host='localhost', port=8080, debug=True, reloader=True)

# comentar la línea anterior y descomentar la sigiuente para usar en PythonAnywhere
# application = default_app()

