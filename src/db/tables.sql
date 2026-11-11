CREATE TABLE region (
  id serial PRIMARY KEY,
  nombre varchar(128) UNIQUE	
);

CREATE TABLE estacion (
  id serial PRIMARY KEY,
  id_region integer,
  nombre varchar(512) unique,
  activa boolean,
  ubicacion varchar(512),
  url text,
  CONSTRAINT fk_region
    FOREIGN KEY(id_region) 
      REFERENCES region(id)
);

CREATE TABLE datos_estacion (
  id serial PRIMARY KEY,
  id_estacion integer,
  fecha_creacion timestamptz NOT NULL,
  temp real,
  tmax real,
  hr real,
  CONSTRAINT fk_estacion
    FOREIGN KEY(id_estacion)
      REFERENCES estacion(id)
);
