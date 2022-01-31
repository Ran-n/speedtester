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
    "id"            TEXT UNIQUE NOT NULL,
    "url"           TEXT UNIQUE NOT NULL,
    "lat"           REAL NOT NULL,
    "lonx"          REAL NOT NULL,
    "nome"          TEXT UNIQUE NOT NULL,
    "sponsor"       TEXT NOT NULL,
    "id_speedtest"  INTEGER UNIQUE NOT NULL,
    "host"          TEXT UNIQUE NOT NULL,
    "distancia"     REAL NOT NULL,
    "latencia"      REAL NOT NULL,
    "id_estado"     TEXT NOT NULL,
    CONSTRAINT servidorPK PRIMARY KEY ("id"),
    CONSTRAINT servidorFK1 FOREIGN KEY ("id_estado") REFERENCES "estado" ("id") ON UPDATE CASCADE MATCH [FULL]
);

CREATE TABLE IF NOT EXISTS "config"(
    "id"            TEXT UNIQUE NOT NULL,
    "max subida"    INTEGER NOT NULL,
    CONSTRAINT configPK PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "operacion"(
    "id"    TEXT UNIQUE NOT NULL,
    "nome"  TEXT UNIQUE NOT NULL,
    CONSTRAINT operacionPK PRIMARY KEY ("id")
);

INSERT OR IGNORE INTO "operacion" ("id", "nome") VALUES ("QYq8hDvAPyHurgsFel_Xnd5_VL-gCRuo", "subida");
INSERT OR IGNORE INTO "operacion" ("id", "nome") VALUES ("p_2olz_AwACNU4XfBQ1o75w9g1vB6Dbg", "baixada");

CREATE TABLE IF NOT EXISTS "tamanho"(
    "id_config"     TEXT UNIQUE NOT NULL,
    "id_operacion"  TEXT UNIQUE NOT NULL,
    "valor"         INTEGER NOT NULL,
    CONSTRAINT tamanhoPK PRIMARY KEY ("id_config", "id_operacion", "valor")
    CONSTRAINT tamanhoFK1 FOREIGN KEY ("id_config") REFERENCES "config" ("id") ON UPDATE CASCADE MATCH [FULL],
    CONSTRAINT tamanhoFK2 FOREIGN KEY ("id_operacion") REFERENCES "operacion" ("id") ON UPDATE CASCADE MATCH [FULL]
);

CREATE TABLE IF NOT EXISTS "count"(
    "id_config"     TEXT UNIQUE NOT NULL,
    "id_operacion"  TEXT UNIQUE NOT NULL,
    "valor"         INTEGER NOT NULL,
    CONSTRAINT countPK PRIMARY KEY ("id_config", "id_operacion", "valor")
    CONSTRAINT countFK1 FOREIGN KEY ("id_config") REFERENCES "config" ("id") ON UPDATE CASCADE MATCH [FULL],
    CONSTRAINT countFK2 FOREIGN KEY ("id_operacion") REFERENCES "operacion" ("id") ON UPDATE CASCADE MATCH [FULL]
);

CREATE TABLE IF NOT EXISTS "fio"(
    "id_config"     TEXT UNIQUE NOT NULL,
    "id_operacion"  TEXT UNIQUE NOT NULL,
    "valor"         INTEGER NOT NULL,
    CONSTRAINT fioPK PRIMARY KEY ("id_config", "id_operacion", "valor"),
    CONSTRAINT fioFK1 FOREIGN KEY ("id_config") REFERENCES "config" ("id") ON UPDATE CASCADE MATCH [FULL],
    CONSTRAINT fioFK2 FOREIGN KEY ("id_operacion") REFERENCES "operacion" ("id") ON UPDATE CASCADE MATCH [FULL]
);

CREATE TABLE IF NOT EXISTS "length"(
    "id_config"     TEXT UNIQUE NOT NULL,
    "id_operacion"  TEXT UNIQUE NOT NULL,
    "valor"         INTEGER NOT NULL,
    CONSTRAINT lengthPK PRIMARY KEY ("id_config", "id_operacion", "valor"),
    CONSTRAINT lengthFK1 FOREIGN KEY ("id_config") REFERENCES "config" ("id") ON UPDATE CASCADE MATCH [FULL],
    CONSTRAINT lengthFK2 FOREIGN KEY ("id_operacion") REFERENCES "operacion" ("id") ON UPDATE CASCADE MATCH [FULL]
);

CREATE TABLE IF NOT EXISTS "servidor_ignorado"(
    "id_config"     TEXT UNIQUE NOT NULL,
    "id_servidor"   TEXT UNIQUE NOT NULL,
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
    CONSTRAINT conexionPK PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "distancia"(
    "id_conexion"        TEXT UNIQUE NOT NULL,
    "distancia"          INTEGER NOT NULL,
    CONSTRAINT tipo_conexionPK PRIMARY KEY ("id_conexion", "distancia"),
    CONSTRAINT distanciaFK1 FOREIGN KEY ("id_conexion") REFERENCES "conexion" ("id") ON UPDATE CASCADE MATCH [FULL]
);

CREATE TABLE IF NOT EXISTS "situacion_servidor"(
    "id"        TEXT UNIQUE NOT NULL,
    "nome"      TEXT UNIQUE NOT NULL,
    CONSTRAINT tipo_servidorPK PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "proba"(
    "id"                    INTEGER UNIQUE NOT NULL,
    "data"                  TEXT NOT NULL,
    "vel_baixada"           INTEGER NOT NULL,
    "bytes_recibidos"       INTEGER NOT NULL,
    "vel_subida"            INTEGER NOT NULL,
    "bytes_enviados"        INTEGER NOT NULL,
    "ping"                  INTEGER NOT NULL,
    "share"                 TEXT NOT NULL,
    "id_servidor"           TEXT NOT NULL,
    "id_cliente"            TEXT NOT NULL,
    "id_config"             TEXT NOT NULL,
    "id_conexion"           TEXT NOT NULL,
    CONSTRAINT probaPK PRIMARY KEY ("id"),
    CONSTRAINT probaFK1 FOREIGN KEY ("id_servidor") REFERENCES "servidor" ("id") ON UPDATE CASCADE MATCH [FULL],
    CONSTRAINT probaFK2 FOREIGN KEY ("id_cliente") REFERENCES "cliente" ("id") ON UPDATE CASCADE MATCH [FULL],
    CONSTRAINT probaFK3 FOREIGN KEY ("id_config") REFERENCES "config" ("id") ON UPDATE CASCADE MATCH [FULL],
    CONSTRAINT probaFK4 FOREIGN KEY ("id_conexion") REFERENCES "conexion" ("id") ON UPDATE CASCADE MATCH [FULL]
);

CREATE TABLE IF NOT EXISTS "situacion_servidor-proba"(
    "id_proba"              TEXT NOT NULL,
    "id_situacion_servidor" TEXT NOT NULL,
    CONSTRAINT probaPK PRIMARY KEY ("id_proba", "id_situacion_servidor"),
    CONSTRAINT probaFK1 FOREIGN KEY ("id_proba") REFERENCES "proba" ("id") ON UPDATE CASCADE MATCH [FULL],
    CONSTRAINT probaFK2 FOREIGN KEY ("id_situacion_servidor") REFERENCES "situacion_servidor" ("id") ON UPDATE CASCADE MATCH [FULL]
);