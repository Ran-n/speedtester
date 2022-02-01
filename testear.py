#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Autor:  	Ran#
#+ Creado: 	2022/02/01 20:59:53.807311
#+ Editado:	2022/02/01 23:37:39.212636
# ------------------------------------------------------------------------------
import sqlite3
from sqlite3 import Cursor, IntegrityError
import os
from speedtest import Speedtest
from secrets import token_urlsafe

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

def get_chave() -> str:
    """
    Retorna un catex aleatorio de 32 caracteres que se usará como id
    """
    return token_urlsafe(24)

# ------------------------------------------------------------------------------

def get_estado(cur: Cursor, codigo: str, nome: str) -> str:
    id_estado = cur.execute(f'select id from estado where codigo = "{codigo}"').fetchone()

    # se non devolve nada
    if not id_estado:
        # ate que non de erro
        while True:
            try:
                id_estado = get_chave()
                cur.execute('insert into estado ("id", "codigo", "nome") '\
                        f'values ("{id_estado}", "{codigo}", "{nome}")')
            except Exception as e:
                print(e)
                pass
            else:
                break
    else:
        id_estado = id_estado[0]

    return id_estado

def gardar_servers(cur: Cursor, s: Speedtest) -> None:
    for distancia in s.servers:
        for server in s.servers[distancia]:
            id_estado = get_estado(cur, server['cc'], server['country'])

            sentenza = ('insert into servidor ("id", "url", "lat", "lonx", '\
                    '"nome", "sponsor",  "host", "distancia", "id_estado") values ('\
                    f'"{server["id"]}", "{server["url"]}", "{server["lat"]}", "{server["lon"]}", '\
                    f'"{server["name"]}", "{server["sponsor"]}", "{server["host"]}", '\
                    f'"{server["d"]}", "{id_estado}")')

            try:
                cur.execute(sentenza)
            except IntegrityError:
                pass
            except Exception as e:
                print()
                print(f'*** Erro {e}')
                print(f'*** Sentenza {sentenza}')
                print()

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

    # gardamos os servers
    gardar_servers(cur, s)

    con.commit()
    con.close()

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    main()

# ------------------------------------------------------------------------------
