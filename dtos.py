#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Autor:  	Ran#
#+ Creado: 	2022/02/01 21:42:24.569281
#+ Editado:	2022/02/02 23:24:24.391549
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

@dataclass
class Estado:
    id_: str = field(default=get_chave(), init=False, repr=False)
    codigo: str
    nome: str

    def __str__(self):
        return f'{self.nome} ({self.codigo})'

@dataclass
class Servidor:
    id_: str
    url: str
    lat: float
    lonx: float
    nome: str
    sponsor: str
    host: str
    distancia: float
    id_estado: str
    latencia: float = 0.0

    def __str__(self):
        return f'{self.nome} ({self.latencia},{self.distancia})'

@dataclass
class ISP:
    id_: str = field(default=get_chave(), init=False, repr=False)
    nome: str
    rating: float
    dlavg: str
    ulavg: str
    loggedin: str
    id_estado: str

@dataclass
class Cliente:
    id_: str = field(default=get_chave(), init=False, repr=False)
    ip: str
    lat: float
    lonx: float
    rating: float
    id_isp: str

@dataclass
class Config:
    id_: str = field(default=get_chave(), init=False, repr=False)
    max_subida: int

@dataclass
class Tamanho:
    id_config: str
    id_operacion: str
    valor: int

@dataclass
class Count:
    id_config: str
    id_operacion: str
    valor: int

@dataclass
class Fio:
    id_config: str
    id_operacion: str
    valor: int

@dataclass
class Length:
    id_config: str
    id_operacion: str
    valor: int

@dataclass
class Proba:
    id_: str = field(default=get_chave(), init=False, repr=False)
    data: str
    timestamp: str
    vel_baixada: int
    bytes_recibidos: int
    vel_subida: int
    bytes_enviados: int
    ping: float
    distancia: float
    share: str
    id_servidor: str
    id_cliente: str
    id_config: str

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    e = Estado('AA', 'Andalucia')
    print(e)
    print(e.id_)
