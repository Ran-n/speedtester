#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Autor:  	Ran#
#+ Creado: 	2022/02/01 21:42:24.569281
#+ Editado:	2022/02/01 22:20:07.289917
# ------------------------------------------------------------------------------
from dataclasses import dataclass, field
from secrets import token_urlsafe
# ------------------------------------------------------------------------------

def get_chave() -> str:
    """
    Retorna un catex aleatorio de 32 caracteres que se usará como id
    """
    return token_urlsafe(24)

# ------------------------------------------------------------------------------

@dataclass()
class Estado:
    id_: str = field(default=get_chave(), init=False, repr=False)
    codigo: str
    nome: str

    def __str__(self):
        return f'{self.nome} ({self.codigo})'

@dataclass()
class Servidor:
    id_: str = field(default=get_chave(), init=False, repr=False)
    url: str
    lat: float
    lonx: float
    nome: str
    sponsor: str
    id_speedtest: int
    host: str
    distancia: float
    latencia: float = 0.0
    id_estado: str

    def __str__(self):
        return f'{self.nome} ({self.latencia},{self.distancia})'

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    e = Estado('AA', 'Andalucia')
    print(e)
    print(e.id_)
