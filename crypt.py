#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Autor:   Ran#
#+ Creado:  2022/01/28 20:03:05.222960
#+ Editado:	2022/02/03 18:52:07.210477
# ------------------------------------------------------------------------------
import sys
import os

from uteis.ficheiro import cargarJson
# ------------------------------------------------------------------------------

def cript(operacion: str, uid: str, fich_entrada: str, fich_saida: str) -> None:
    comando = f'gpg {operacion} --armor -r {uid} -o {fich_saida} {fich_entrada}'

    if DEBUG: print('$: '+comando)

    try:
        os.system(comando)
    except Exception as e:
        raise e
    else:
        try:
            os.remove(fich_entrada)
        except OSError:
            pass

# ------------------------------------------------------------------------------

def main(opcion_introducida):
    cnf = cargarJson('./.cnf')

    ops = {
        'e': ['-se', cnf['script insert db'], cnf['script insert db encrypted']],
        'd': ['-d', cnf['script insert db encrypted'], cnf['script insert db']]
        }

    try:
        opcion = ops[opcion_introducida]
    except KeyError:
        raise Exception(f'{opcion_introducida} non é considerada unha opción.')

    cript(opcion[0], cnf['uid_gpg'], opcion[1], opcion[2])

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    DEBUG = True

    main(sys.argv[1])

# ------------------------------------------------------------------------------
