CREATE TABLE IF NOT EXISTS "estado"(
    "id"        TEXT UNIQUE NOT NULL,
    "codigo"    TEXT UNIQUE NOT NULL,
    "nome"      TEXT UNIQUE NOT NULL,
    CONSTRAINT estadoPK PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "isp"(
    "id"        TEXT UNIQUE NOT NULL,
    "nome"      TEXT UNIQUE NOT NULL,
    "rating"    REAL NOT NULL,
    "dlavg"     TEXT NOT NULL,
    "ulavg"     TEXT NOT NULL,
    "loggedin"  TEXT NOT NULL,
    "id_estado" TEXT NOT NULL,
    CONSTRAINT ispPK PRIMARY KEY ("id"),
    CONSTRAINT ispFK1 FOREIGN KEY ("id_estado") REFERENCES "estado" ("id") ON UPDATE CASCADE MATCH [FULL]
);

CREATE TABLE IF NOT EXISTS "cliente"(
    "id"            TEXT UNIQUE NOT NULL,
    "ip"            TEXT NOT NULL,
    "lat"           REAL not NULL,
    "lonx"          REAL not NULL,
    "rating"        REAL NOT NULL,
    "id_isp"        TEXT NOT NULL,
    CONSTRAINT clientePK PRIMARY KEY ("id"),
    CONSTRAINT clienteFK1 FOREIGN KEY ("id_isp") REFERENCES "isp" ("id") ON UPDATE CASCADE MATCH [FULL]
);

CREATE TABLE IF NOT EXISTS "servidor"(
    "id"            INTEGER UNIQUE NOT NULL,
    "url"           TEXT UNIQUE NOT NULL,
    "lat"           REAL NOT NULL,
    "lonx"          REAL NOT NULL,
    "nome"          TEXT NOT NULL,
    "sponsor"       TEXT NOT NULL,
    "host"          TEXT NOT NULL,
    "distancia"     REAL NOT NULL,
    "id_estado"     TEXT NOT NULL,
    CONSTRAINT servidorPK PRIMARY KEY ("id"),
    CONSTRAINT servidorFK1 FOREIGN KEY ("id_estado") REFERENCES "estado" ("id") ON UPDATE CASCADE MATCH [FULL]
);

CREATE TABLE IF NOT EXISTS "config"(
    "id"            TEXT UNIQUE NOT NULL,
    "max_subida"    INTEGER UNIQUE NOT NULL,
    CONSTRAINT configPK PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "operacion"(
    "id"    TEXT UNIQUE NOT NULL,
    "nome"  TEXT UNIQUE NOT NULL,
    CONSTRAINT operacionPK PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "tamanho"(
    "id_config"     TEXT NOT NULL,
    "id_operacion"  TEXT NOT NULL,
    "valor"         INTEGER UNIQUE NOT NULL,
    CONSTRAINT tamanhoPK PRIMARY KEY ("id_config", "id_operacion", "valor")
    CONSTRAINT tamanhoFK1 FOREIGN KEY ("id_config") REFERENCES "config" ("id") ON UPDATE CASCADE MATCH [FULL],
    CONSTRAINT tamanhoFK2 FOREIGN KEY ("id_operacion") REFERENCES "operacion" ("id") ON UPDATE CASCADE MATCH [FULL]
);

CREATE TABLE IF NOT EXISTS "count"(
    "id_config"     TEXT NOT NULL,
    "id_operacion"  TEXT NOT NULL,
    "valor"         INTEGER UNIQUE NOT NULL,
    CONSTRAINT countPK PRIMARY KEY ("id_config", "id_operacion", "valor")
    CONSTRAINT countFK1 FOREIGN KEY ("id_config") REFERENCES "config" ("id") ON UPDATE CASCADE MATCH [FULL],
    CONSTRAINT countFK2 FOREIGN KEY ("id_operacion") REFERENCES "operacion" ("id") ON UPDATE CASCADE MATCH [FULL]
);

CREATE TABLE IF NOT EXISTS "fio"(
    "id_config"     TEXT NOT NULL,
    "id_operacion"  TEXT NOT NULL,
    "valor"         INTEGER UNIQUE NOT NULL,
    CONSTRAINT fioPK PRIMARY KEY ("id_config", "id_operacion", "valor"),
    CONSTRAINT fioFK1 FOREIGN KEY ("id_config") REFERENCES "config" ("id") ON UPDATE CASCADE MATCH [FULL],
    CONSTRAINT fioFK2 FOREIGN KEY ("id_operacion") REFERENCES "operacion" ("id") ON UPDATE CASCADE MATCH [FULL]
);

CREATE TABLE IF NOT EXISTS "length"(
    "id_config"     TEXT NOT NULL,
    "id_operacion"  TEXT NOT NULL,
    "valor"         INTEGER UNIQUE NOT NULL,
    CONSTRAINT lengthPK PRIMARY KEY ("id_config", "id_operacion", "valor"),
    CONSTRAINT lengthFK1 FOREIGN KEY ("id_config") REFERENCES "config" ("id") ON UPDATE CASCADE MATCH [FULL],
    CONSTRAINT lengthFK2 FOREIGN KEY ("id_operacion") REFERENCES "operacion" ("id") ON UPDATE CASCADE MATCH [FULL]
);

CREATE TABLE IF NOT EXISTS "servidor_ignorado"(
    "id_config"     TEXT NOT NULL,
    "id_servidor"   TEXT NOT NULL,
    CONSTRAINT lengthPK PRIMARY KEY ("id_config", "id_servidor"),
    CONSTRAINT servidor_ignoradoFK1 FOREIGN KEY ("id_config") REFERENCES "config" ("id") ON UPDATE CASCADE MATCH [FULL],
    CONSTRAINT servidor_ignoradoFK2 FOREIGN KEY ("id_servidor") REFERENCES "servidor" ("id") ON UPDATE CASCADE MATCH [FULL]
);

CREATE TABLE IF NOT EXISTS "router"(
    "id"            TEXT UNIQUE NOT NULL,
    "nome"          TEXT UNIQUE NOT NULL,
    "descricion"    TEXT,
    CONSTRAINT routerPK PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "conexion"(
    "id"        TEXT UNIQUE NOT NULL,
    "nome"      TEXT NOT NULL,
    "tipo"      TEXT NOT NULL,
    "id_router" TEXT NOT NULL,
    CONSTRAINT conexionPK PRIMARY KEY ("id"),
    CONSTRAINT conexionFK1 FOREIGN KEY ("id_router") REFERENCES "router" ("id") ON UPDATE CASCADE MATCH [FULL]
);

CREATE TABLE IF NOT EXISTS "distancia"(
    "id_conexion"   TEXT UNIQUE NOT NULL,
    "distancia"     INTEGER NOT NULL,
    "hops"          INTEGER NOT NULL,
    CONSTRAINT tipo_conexionPK PRIMARY KEY ("id_conexion", "distancia"),
    CONSTRAINT distanciaFK1 FOREIGN KEY ("id_conexion") REFERENCES "conexion" ("id") ON UPDATE CASCADE MATCH [FULL]
);

CREATE TABLE IF NOT EXISTS "proba"(
    "id"                    INTEGER UNIQUE NOT NULL,
    "data"                  TEXT NOT NULL,
    "timestamp"             TEXT NOT NULL,
    "vel_baixada"           INTEGER NOT NULL,
    "bytes_recibidos"       INTEGER NOT NULL,
    "vel_subida"            INTEGER NOT NULL,
    "bytes_enviados"        INTEGER NOT NULL,
    "ping"                  REAL NOT NULL,
    "distancia"             REAL NOT NULL,
    "share"                 TEXT,
    "id_servidor"           TEXT NOT NULL,
    "id_cliente"            TEXT NOT NULL,
    "id_config"             TEXT NOT NULL,
    CONSTRAINT probaPK PRIMARY KEY ("id"),
    CONSTRAINT probaFK1 FOREIGN KEY ("id_servidor") REFERENCES "servidor" ("id") ON UPDATE CASCADE MATCH [FULL],
    CONSTRAINT probaFK2 FOREIGN KEY ("id_cliente") REFERENCES "cliente" ("id") ON UPDATE CASCADE MATCH [FULL],
    CONSTRAINT probaFK3 FOREIGN KEY ("id_config") REFERENCES "config" ("id") ON UPDATE CASCADE MATCH [FULL]
);
