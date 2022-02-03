INSERT OR IGNORE INTO "estado" ("id", "codigo", "nome") VALUES ("x6wCCxbaMzyYEhGKpljtHWMwDHt1wInP", "ES", "Espanha");
INSERT OR IGNORE INTO "estado" ("id", "codigo", "nome") VALUES ("g2lFdJbsCsXHjDa62tzNMEcUChWQtpMB", "PT", "Portugal");

INSERT OR IGNORE INTO "operacion" ("id", "nome") VALUES ("QYq8hDvAPyHurgsFel_Xnd5_VL-gCRuo", "subida");
INSERT OR IGNORE INTO "operacion" ("id", "nome") VALUES ("p_2olz_AwACNU4XfBQ1o75w9g1vB6Dbg", "baixada");

INSERT OR IGNORE INTO "router" ("id", "nome", "descricion") VALUES ("6R839DL7ZSmAbMEiVk0peLjvSuf8x2HH", "R2", "O que nos deu R tras facer o cambio a fibra óptica");

INSERT OR IGNORE INTO "conexion" ("id", "nome", "tipo", "id_router") VALUES ("h9u1M83RZthZeWa8zQDSK_egHJ4fI-Ce", "O Rochazo do Rochas", "wifi", "6R839DL7ZSmAbMEiVk0peLjvSuf8x2HH");
INSERT OR IGNORE INTO "conexion" ("id", "nome", "tipo", "id_router") VALUES ("TQwRUgLDe7ldZ5uzJzKm0-_y1otq_nZr", "O Rochazo do Rochas", "ethernet", "6R839DL7ZSmAbMEiVk0peLjvSuf8x2HH");

INSERT OR IGNORE INTO "distancia" ("id_conexion", "distancia", "hops") VALUES ("TQwRUgLDe7ldZ5uzJzKm0-_y1otq_nZr", "0", "2");

INSERT OR IGNORE INTO "dispositivo" ("id", "nome") VALUES ("pQdHO7u5uwyx6yXGp4pSF9xZgIe6JMLh", "FrIC");
INSERT OR IGNORE INTO "dispositivo" ("id", "nome") VALUES ("UhH33RFhcNOFuI-oJ6Blp5h8G-IU0Fax", "Touro");
