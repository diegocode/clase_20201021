#!/usr/bin/python
# -*- coding: utf-8 -*-
from bottle import default_app, route, request, template, static_file

import datetime

@route('/datain')
def guardar_datos():
    """
        recibe y guarda los datos del request de clientes
    """
    error_datain = 0

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
    # una línea solamente ! --> reemplazar por insert a BBDD
    try:
        f = open("datos.csv", "w")
        linea_datos = temp + ";" + hume + ";" + sens_nro + ";" + tstamp + ";" + ip_orig + "\n"
        f.write(linea_datos)
        f.close()
    except:
        pass


@route('/')
def inicio():
    """
        muestra home
    """
    return template('index_base.html')


@route('/ver')
def ver_datos():
    """
        procesa el pedido del browser
        lee los datos del archivo (reemplazar por BBDD!!)
        y los envía como texto
    """
    f = open("datos.csv", "r")
    medicion = f.readline().split(";")
    f.close()

    try:
        temp = float(medicion[0])
        hume = float(medicion[1])
        snum = medicion[2]
        tstm = medicion[3]
        ipor = medicion[4]
    except:
        print(medicion)

    return "%5.2f %5.2f %3s %s %s" % (temp, hume, snum, tstm, ipor)


@route('/contacto')
def contacto():
	return "contacto"


@route('/<filepath:path>')
def server_static(filepath):    
    """ necesario para archivos estáticos (.css, imagenes, etc.) """
    return static_file(filepath, root='.')


# ejecuta server de desarrollo
run(host='localhost', port=8080, debug=True, reloader=True)

# comentar la línea anterior y descomentar la sigiuente para usar en "prod"
# application = default_app()

