#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Autor:  	Ran#
#+ Creado: 	2022/02/01 20:59:53.807311
#+ Editado:	2022/02/03 18:37:01.414345
# ------------------------------------------------------------------------------
import sqlite3
from sqlite3 import Cursor, IntegrityError
import os
from speedtest import Speedtest
from secrets import token_urlsafe
from typing import List, Union
from datetime import datetime

from uteis.ficheiro import cargarFich, cargarJson

from dtos import ISP, Cliente, Config, Proba, Servidor
# ------------------------------------------------------------------------------

def script_db(cur: Cursor, fich: str) -> None:
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

def get_id_estado(cur: Cursor, codigo: str, nome: str = '') -> str:
    id_estado = cur.execute(f'select id from estado where codigo = "{codigo}"').fetchone()

    # se non devolve nada
    if not id_estado:
        # ate que non de erro
        while True:
            try:
                id_estado = get_chave()
                cur.execute('insert into estado ("id", "codigo", "nome") '\
                        f'values ("{id_estado}", "{codigo}", "{nome}")')
            except IntegrityError:
                if DEBUG_ALL: print('\n*** O estado xa estaba gardado, actualizando o nome se compete')
                # se xa existe e se meteu un nome, mira se xa estaba metido sen nome e nese caso ponllo
                if nome != '':
                    cur.execute(f'update estado set "nome"="{nome}" where "codigo"="{codigo}" and "nome"=""' )
            except Exception as e:
                if DEBUG:
                    print('\n*** ERRO na función get_id_estado')
                else:
                    print()
                print(f'*** ERRO: {e}')
            else:
                break
    else:
        id_estado = id_estado[0]

    return id_estado

def gardar_servers(cur: Cursor, s: Speedtest) -> None:
    for distancia in s.servers:
        for server in s.servers[distancia]:
            id_estado = get_id_estado(cur, server['cc'], server['country'])

            sentenza = ('insert into servidor ("id", "url", "lat", "lonx", '\
                    '"nome", "sponsor",  "host", "distancia", "id_estado") values ('\
                    f'"{server["id"]}", "{server["url"]}", "{server["lat"]}", "{server["lon"]}", '\
                    f'"{server["name"]}", "{server["sponsor"]}", "{server["host"]}", '\
                    f'"{server["d"]}", "{id_estado}")')

            try:
                cur.execute(sentenza)
            except IntegrityError:
                vars_db = ['url', 'lat', 'lonx', 'nome', 'sponsor', 'host', 'distancia']
                vars_st = ['url', 'lat', 'lon', 'name', 'sponsor', 'host', 'd']

                if DEBUG_ALL: print('\n*** O servidor xa estaba gardado, actualizando {vars_db} se compete')

                #for var_db, var_st in zip(vars_db, vars_st):
                #    cur.execute(f'update servidor set "{var_db}"="{var_st}" where "{var_db}"<>"{var_st}" and id="{server["id"]}"')
            except Exception as e:
                if DEBUG:
                    print('\n*** ERRO na función gardar_tamanhos na parte de sacar os ids')
                    print(f'\n*** Sentenza: {sentenza}')
                else:
                    print()
                print(f'*** ERRO: {e}')

def gardar_server(cur: Cursor, s: Servidor) -> str:
    try:
        cur.execute('insert into servidor ("id", "url", "lat", "lonx", "nome", '\
                '"sponsor", "host", "distancia", "id_estado") values ('\
                f'"{s.id_}", "{s.url}", "{s.lat}", "{s.lonx}", "{s.nome}", '\
                f'"{s.sponsor}", "{s.host}", "{s.distancia}", "{s.id_estado}")')
    except IntegrityError:
        if DEBUG_ALL: print('\n*** O servidor xa estaba gardado')
    except Exception as e:
        if DEBUG:
            print('\n*** ERRO na función gardar_server')
        else:
            print()
        print(f'*** ERRO: {e}')

    return s.id_

def gardar_isp(cur: Cursor, isp: ISP) -> str:
    try:
        cur.execute('insert into isp ("id", "nome", "rating", "dlavg", "ulavg", "loggedin", "id_estado") '\
                f'values ("{isp.id_}", "{isp.nome}", "{isp.rating}", "{isp.dlavg}", "{isp.ulavg}", '\
                f'"{isp.loggedin}", "{isp.id_estado}")')
    except IntegrityError:
        if DEBUG_ALL: print('\n*** A isp xa estaba gardada')
        # se xa existe collo o id
        return cur.execute(f'select id from isp where "nome"="{isp.nome}"').fetchone()[0]
    except Exception as e:
        if DEBUG:
            print('\n*** ERRO na función gardar_isp')
        else:
            print()
        print(f'*** ERRO: {e}')

    return isp.id_

def gardar_cliente(cur: Cursor, c: Cliente) -> str:
    id_cliente = cur.execute(f'select id from cliente where ip="{c.ip}" and lat="{c.lat}" and lonx="{c.lonx}"').fetchone()
    if not id_cliente:
        try:
            id_cliente = [c.id_]
            cur.execute('insert into cliente ("id", "ip", "lat", "lonx", "rating", "id_isp") '\
                    f'values ("{c.id_}", "{c.ip}", "{c.lat}", "{c.lonx}", "{c.rating}", "{c.id_isp}")')
        except IntegrityError:
            if DEBUG_ALL: print('\n*** ERRO de integridade na función gardar_cliente')
        except Exception as e:
            if DEBUG:
                print('\n*** ERRO na función gardar_tamanhos na parte de sacar os ids')
            else:
                print()
            print(f'*** ERRO: {e}')

    return id_cliente[0]

def gardar_config(cur: Cursor, cnf: Config) -> str:
    try:
        cur.execute('insert into config ("id", "max_subida") '\
            f'values ("{cnf.id_}", "{cnf.max_subida}")')
    except IntegrityError:
        if DEBUG_ALL: print('\n*** A config xa existe')
        # se xa existe collo o id
        return cur.execute(f'select id from config where "max_subida"="{cnf.max_subida}"').fetchone()[0]
    except Exception as e:
        print(e)

    return cnf.id_

def gardar_config_related(cur: Cursor, taboa: str, cnf_id:str, lst_subida: List[int], lst_baixada: List[int]) -> None:
    if type(lst_subida) != list:
        lst_subida = [lst_subida]
    if type(lst_baixada) != list:
        lst_baixada = [lst_baixada]

    try:
       id_subida = cur.execute('select id from operacion where nome="subida"').fetchone()[0]
       id_baixada = cur.execute('select id from operacion where nome="baixada"').fetchone()[0]
    except:
        if DEBUG: print('\n*** ERRO na función gardar_tamanhos na parte de sacar os ids')
        raise Exception('A táboa operación ten que ter unha columna chamada subida e outra baixada')

    # insert subidas
    for ele in lst_subida:
        try:
            cur.execute(f'insert into {taboa} ("id_config", "id_operacion", "valor") '\
                        f'values ("{cnf_id}", "{id_subida}", "{ele}")')
        except IntegrityError:
            if DEBUG_ALL: print('\n*** ERRO de integridade na funcion gardar_tamanhos na parte de subidas')
        except Exception as e:
            if DEBUG: print('\n*** ERRO na función gardar_tamanhos na parte de subidas')
            print(f'*** ERRO: {e}')

    # insert baixadas
    for ele in lst_baixada:
        try:
            cur.execute(f'insert into {taboa} ("id_config", "id_operacion", "valor") '\
                        f'values ("{cnf_id}", "{id_baixada}", "{ele}")')
        except IntegrityError:
            if DEBUG_ALL: print('\n*** ERRO de integridade na funcion gardar_tamanhos na parte de baixadas')
        except Exception as e:
            if DEBUG: print('\n*** ERRO na función gardar_tamanhos na parte de baixadas')
            print(f'*** ERRO: {e}')

def gardar_proba(cur: Cursor, p: Proba) -> None:
    try:
        cur.execute('insert into proba ("data", "timestamp", "vel_baixada", '\
                '"bytes_recibidos", "vel_subida", "bytes_enviados", "ping", '\
                '"distancia", "share", "id_servidor", "id_cliente", "id_config", '\
                '"id_conexion", "id_dispositivo") '\
                f'values ("{p.data}", "{p.timestamp}", "{p.vel_baixada}", '\
                f'"{p.bytes_recibidos}", "{p.vel_subida}", "{p.bytes_enviados}", '\
                f'"{p.ping}", "{p.distancia}", "{p.share}", "{p.id_servidor}", '\
                f'"{p.id_cliente}", "{p.id_config}", "{p.id_conexion}", "{p.id_dispositivo}")')
    except IntegrityError:
        if DEBUG_ALL: print('\n*** Erro de integridade na función gardar_proba')
    except Exception as e:
        if DEBUG:
            print('\n*** ERRO na función gardar_proba')
        else:
            print()
        print(f'*** ERRO: {e}')

def select_opcion(cur: Cursor, taboa) -> Union[str, int]:
    while True:
        select = cur.execute(f'select * from {taboa}')
        cabeceiras = select.description
        select = select.fetchall()


        print('\n -- Selección --\n')
        for ele in cabeceiras:
            print(f'{ele[0]}', end='\t')
        print('\n-----------------------------------------------------------------------------------------')
        for index, ele in enumerate(select, 1):
            print(f'{index}. {ele}')

        seleccion = input('> Selección: ')
        if seleccion.isdigit() and int(seleccion) <= index and int(seleccion) > 0:
            id_opcion = select[int(seleccion)-1][0]
            break
        else:
            print()
    return id_opcion

def main():
    cnf = cargarJson('.cnf')

    if not os.path.isfile(cnf['db']):
        print()
        print('Tes que ter a táboa de operacións con unha de subida e outra de baixada')
        print('Tes que ter a táboa de router con un polo menos')
        print('Tes que ter a táboa de conexion con unha polo menos')
        print('Tes que ter a táboa de distancia con unha polo menos')
        print('Tes que ter a táboa de dispositivo con un polo menos')

    con = sqlite3.connect(cnf['db'])
    cur = con.cursor()

    # crear a db
    script_db(cur, cnf['script create db'])
    # facer os inserts inicais
    script_db(cur, cnf['script insert db'])

    # preguntaselle ó usuario que conexión e dispositivo está usando
    id_conexion = select_opcion(cur, 'conexion')
    id_dispositivo = select_opcion(cur, 'dispositivo')

    s = Speedtest()

    # primeiro isto por deficiencia do paquete
    s = get_closest_servers(s)
    s.get_servers()

    # gardamos os servers
    gardar_servers(cur, s)

    # gardar os datos da isp
    isp = ISP(
            s.config['client']['isp'],
            s.config['client']['isprating'],
            s.config['client']['ispdlavg'],
            s.config['client']['ispulavg'],
            s.config['client']['loggedin'],
            get_id_estado(cur, s.config['client']['country'])
            )
    isp.id_ = gardar_isp(cur, isp)

    # gardar os datos do cliente
    cliente = Cliente(
            s.config['client']['ip'],
            s.config['client']['lat'],
            s.config['client']['lon'],
            s.config['client']['rating'],
            isp.id_
            )
    cliente.id_ = gardar_cliente(cur, cliente)

    # gardar a config
    config = Config(s.config['upload_max'])
    config.id_ = gardar_config(cur, config)

    #gardar_servidores_ignorados(cur, s.config['ignore_servers'])

    gardar_config_related(cur, 'tamanho', config.id_, s.config['sizes']['upload'], s.config['sizes']['download'])
    gardar_config_related(cur, 'count', config.id_, s.config['counts']['upload'], s.config['counts']['download'])
    gardar_config_related(cur, 'fio', config.id_, s.config['threads']['upload'], s.config['threads']['download'])
    gardar_config_related(cur, 'length', config.id_, s.config['length']['upload'], s.config['length']['download'])

    # coller o mellor servidor
    s.get_best_server()

    mellor_servidor = Servidor(
            s.best['id'],
            s.best['url'],
            s.best['lat'],
            s.best['lon'],
            s.best['name'],
            s.best['sponsor'],
            s.best['host'],
            s.best['d'],
            get_id_estado(cur, s.best['cc']),
            s.best['latency']
            )
    gardar_server(cur, mellor_servidor)

    if DEBUG: print('\n*** Iniciando o test de baixada', end='\r')
    s.download()
    if DEBUG:
        print('*** Feito o test de baixada    ')
        print('*** Iniciando o test de subida', end='\r')
    s.upload()
    if DEBUG: print('*** Feito o test de subida    \n')

    results = s.results.dict()
    proba = Proba(
            datetime.now(),
            results['timestamp'],
            results['download'],
            results['bytes_received'],
            results['upload'],
            results['bytes_sent'],
            mellor_servidor.latencia,
            mellor_servidor.distancia,
            results['share'],
            mellor_servidor.id_,
            cliente.id_,
            config.id_,
            id_conexion,
            id_dispositivo
            )
    # a id_conexión está posta de forma fixada polo momento
    gardar_proba(cur, proba)

    con.commit()
    con.close()

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    DEBUG = True
    DEBUG_ALL = False
    main()

# ------------------------------------------------------------------------------
