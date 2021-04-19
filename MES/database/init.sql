CREATE DATABASE ii; 
\c ii; 

CREATE SCHEMA mes; 

CREATE TABLE mes.order (
  order_number INTEGER PRIMARY KEY
); 

CREATE TABLE mes.transform (
  transform_id SERIAL PRIMARY KEY, 
  quantidade INTEGER,
  piece_from TEXT,
  piece_to TEXT, 
  max_delay INTERVAL,
  processing_start TIMESTAMP,
  processing_end TIMESTAMP,  
  penalty INTEGER,
  order_number INTEGER REFERENCES mes.order
); 

CREATE TABLE mes.unload (
  unload_id SERIAL PRIMARY KEY,
  piece_type TEXT,
  destino TEXT,
  quantidade INTEGER,
  order_number INTEGER REFERENCES mes.order
); 

CREATE TABLE mes.piece (
  piece_id SERIAL PRIMARY KEY, 
  initial_state TEXT, 
  piece_type TEXT, 
  location INTEGER[],
  tranform_id INTEGER references mes.transform
); 

CREATE TABLE mes.machine (
  machine_id SERIAL PRIMARY KEY, 
  total_time INTERVAL
); 
