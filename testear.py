#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Autor:  	Ran#
#+ Creado: 	2022/02/01 20:59:53.807311
#+ Editado:	2022/02/01 21:50:35.526246
# ------------------------------------------------------------------------------
import sqlite3
from sqlite3 import Cursor
import os
from speedtest import Speedtest

from uteis.ficheiro import cargarFich, cargarJson
# ------------------------------------------------------------------------------

def script_db(cur: Cursor, fich: str) -> None:
    """
    """
    # se o ficheiro existe executao
    if os.path.isfile(fich):
        cur.executescript(''.join(cargarFich(fich)))

def get_closest_servers(s: Speedtest) -> Speedtest:
    s.closest = []
    s.get_closest_servers()
    return s

# ------------------------------------------------------------------------------

def main():
    cnf = cargarJson('.cnf')

    con = sqlite3.connect(cnf['db'])
    cur = con.cursor()

    # crear a db
    script_db(cur, cnf['script create db'])
    # facer os inserts inicais
    script_db(cur, cnf['script insert db'])


    s = Speedtest()

    # primeiro isto por deficiencia do paquete
    s = get_closest_servers(s)
    s.get_servers()

    for distancia in s.servers:
        for server in s.servers[distancia]:
            server


    con.commit()
    con.close()

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    main()

# ------------------------------------------------------------------------------
