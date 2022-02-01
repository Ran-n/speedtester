#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Autor:  	Ran#
#+ Creado: 	2022/02/01 20:59:53.807311
#+ Editado:	2022/02/01 21:03:20.800969
# ------------------------------------------------------------------------------
import sqlite3
from sqlite3 import Cursor

from uteis.ficheiro import cargarFich, cargarJson
# ------------------------------------------------------------------------------
def crear_db(cur: Cursor) -> None:
    cur.executescript(''.join(cargarFich('script_db.sql')))
# ------------------------------------------------------------------------------
def main():
    cnf = cargarJson('.cnf')

    con = sqlite3.connect(cnf['db'])
    cur = con.cursor()

    crear_db(cur)

    con.commit()
    con.close()
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ------------------------------------------------------------------------------
