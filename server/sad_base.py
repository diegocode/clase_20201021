#!/usr/bin/python
# -*- coding: utf-8 -*-
from bottle import default_app, route, request, template, static_file

import datetime

@route('/datain')
def guardar_datos():
    error_datain = 0

    temp = request.query.tempe
    hume = request.query.hume

    sens_nro = request.query.snum
    if sens_nro == "":
        sens_nro = "0"

    tstamp = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")

    ip_orig = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')

    try:
        f = open("datos.csv", "w")
        linea_datos = temp + ";" + hume + ";" + sens_nro + ";" + tstamp + ";" + ip_orig + "\n"
        f.write(linea_datos)
        f.close()
    except:
        error_datain += 2

@route('/')
def inicio():
    return template('index_base.html')

@route('/ver')
def ver_datos():
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
    """ para archivos estáticos (.css, imagenes, etc.) """
    return static_file(filepath, root='.')


# run(host='localhost', port=8080, debug=True, reloader=True)
application = default_app()




