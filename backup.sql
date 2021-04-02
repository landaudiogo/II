--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1 (Debian 13.1-1.pgdg100+1)
-- Dumped by pg_dump version 13.1 (Debian 13.1-1.pgdg100+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: mes; Type: SCHEMA; Schema: -; Owner: postgres
--
CREATE DATABASE hello;
\c hello

CREATE SCHEMA mes;


ALTER SCHEMA mes OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: machine; Type: TABLE; Schema: mes; Owner: postgres
--

CREATE TABLE mes.machine (
    machine_id integer NOT NULL,
    total_time interval
);


ALTER TABLE mes.machine OWNER TO postgres;

--
-- Name: machine_machine_id_seq; Type: SEQUENCE; Schema: mes; Owner: postgres
--

CREATE SEQUENCE mes.machine_machine_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mes.machine_machine_id_seq OWNER TO postgres;

--
-- Name: machine_machine_id_seq; Type: SEQUENCE OWNED BY; Schema: mes; Owner: postgres
--

ALTER SEQUENCE mes.machine_machine_id_seq OWNED BY mes.machine.machine_id;


--
-- Name: mes_session; Type: TABLE; Schema: mes; Owner: postgres
--

CREATE TABLE mes.mes_session (
    start_epoch integer NOT NULL
);


ALTER TABLE mes.mes_session OWNER TO postgres;

--
-- Name: order; Type: TABLE; Schema: mes; Owner: postgres
--

CREATE TABLE mes."order" (
    number integer NOT NULL
);


ALTER TABLE mes."order" OWNER TO postgres;

--
-- Name: piece; Type: TABLE; Schema: mes; Owner: postgres
--

CREATE TABLE mes.piece (
    piece_id integer NOT NULL,
    location boolean DEFAULT true,
    transform_id integer,
    list_states text[]
);


ALTER TABLE mes.piece OWNER TO postgres;

--
-- Name: piece_piece_id_seq; Type: SEQUENCE; Schema: mes; Owner: postgres
--

CREATE SEQUENCE mes.piece_piece_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mes.piece_piece_id_seq OWNER TO postgres;

--
-- Name: piece_piece_id_seq; Type: SEQUENCE OWNED BY; Schema: mes; Owner: postgres
--

ALTER SEQUENCE mes.piece_piece_id_seq OWNED BY mes.piece.piece_id;


--
-- Name: transform; Type: TABLE; Schema: mes; Owner: postgres
--

CREATE TABLE mes.transform (
    transform_id integer NOT NULL,
    quantity integer,
    "from" text,
    "to" text,
    "time" integer,
    "end" timestamp without time zone,
    penalty integer,
    maxdelay integer,
    order_number integer,
    processed boolean DEFAULT false,
    list_states text[],
    priority real,
    received_time integer
);


ALTER TABLE mes.transform OWNER TO postgres;

--
-- Name: transform_transform_id_seq; Type: SEQUENCE; Schema: mes; Owner: postgres
--

CREATE SEQUENCE mes.transform_transform_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mes.transform_transform_id_seq OWNER TO postgres;

--
-- Name: transform_transform_id_seq; Type: SEQUENCE OWNED BY; Schema: mes; Owner: postgres
--

ALTER SEQUENCE mes.transform_transform_id_seq OWNED BY mes.transform.transform_id;


--
-- Name: transformations_machine; Type: TABLE; Schema: mes; Owner: postgres
--

CREATE TABLE mes.transformations_machine (
    initial_type character varying(2) NOT NULL,
    final_type character varying(2) NOT NULL,
    machine integer
);


ALTER TABLE mes.transformations_machine OWNER TO postgres;

--
-- Name: unload; Type: TABLE; Schema: mes; Owner: postgres
--

CREATE TABLE mes.unload (
    unload_id integer NOT NULL,
    type text,
    destination text,
    quantity integer,
    order_number integer,
    unloaded boolean
);


ALTER TABLE mes.unload OWNER TO postgres;

--
-- Name: unload_unload_id_seq; Type: SEQUENCE; Schema: mes; Owner: postgres
--

CREATE SEQUENCE mes.unload_unload_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mes.unload_unload_id_seq OWNER TO postgres;

--
-- Name: unload_unload_id_seq; Type: SEQUENCE OWNED BY; Schema: mes; Owner: postgres
--

ALTER SEQUENCE mes.unload_unload_id_seq OWNED BY mes.unload.unload_id;


--
-- Name: machine machine_id; Type: DEFAULT; Schema: mes; Owner: postgres
--

ALTER TABLE ONLY mes.machine ALTER COLUMN machine_id SET DEFAULT nextval('mes.machine_machine_id_seq'::regclass);


--
-- Name: piece piece_id; Type: DEFAULT; Schema: mes; Owner: postgres
--

ALTER TABLE ONLY mes.piece ALTER COLUMN piece_id SET DEFAULT nextval('mes.piece_piece_id_seq'::regclass);


--
-- Name: transform transform_id; Type: DEFAULT; Schema: mes; Owner: postgres
--

ALTER TABLE ONLY mes.transform ALTER COLUMN transform_id SET DEFAULT nextval('mes.transform_transform_id_seq'::regclass);


--
-- Name: unload unload_id; Type: DEFAULT; Schema: mes; Owner: postgres
--

ALTER TABLE ONLY mes.unload ALTER COLUMN unload_id SET DEFAULT nextval('mes.unload_unload_id_seq'::regclass);


--
-- Name: machine machine_pkey; Type: CONSTRAINT; Schema: mes; Owner: postgres
--

ALTER TABLE ONLY mes.machine
    ADD CONSTRAINT machine_pkey PRIMARY KEY (machine_id);


--
-- Name: order order_pkey; Type: CONSTRAINT; Schema: mes; Owner: postgres
--

ALTER TABLE ONLY mes."order"
    ADD CONSTRAINT order_pkey PRIMARY KEY (number);


--
-- Name: piece piece_pkey; Type: CONSTRAINT; Schema: mes; Owner: postgres
--

ALTER TABLE ONLY mes.piece
    ADD CONSTRAINT piece_pkey PRIMARY KEY (piece_id);


--
-- Name: mes_session sessions_pkey; Type: CONSTRAINT; Schema: mes; Owner: postgres
--

ALTER TABLE ONLY mes.mes_session
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (start_epoch);


--
-- Name: transform transform_pkey; Type: CONSTRAINT; Schema: mes; Owner: postgres
--

ALTER TABLE ONLY mes.transform
    ADD CONSTRAINT transform_pkey PRIMARY KEY (transform_id);


--
-- Name: transformations_machine transformations_machine_pkey; Type: CONSTRAINT; Schema: mes; Owner: postgres
--

ALTER TABLE ONLY mes.transformations_machine
    ADD CONSTRAINT transformations_machine_pkey PRIMARY KEY (initial_type, final_type);


--
-- Name: unload unload_pkey; Type: CONSTRAINT; Schema: mes; Owner: postgres
--

ALTER TABLE ONLY mes.unload
    ADD CONSTRAINT unload_pkey PRIMARY KEY (unload_id);


--
-- Name: piece piece_tranform_id_fkey; Type: FK CONSTRAINT; Schema: mes; Owner: postgres
--

ALTER TABLE ONLY mes.piece
    ADD CONSTRAINT piece_tranform_id_fkey FOREIGN KEY (transform_id) REFERENCES mes.transform(transform_id);


--
-- Name: transform transform_order_number_fkey; Type: FK CONSTRAINT; Schema: mes; Owner: postgres
--

ALTER TABLE ONLY mes.transform
    ADD CONSTRAINT transform_order_number_fkey FOREIGN KEY (order_number) REFERENCES mes."order"(number);


--
-- Name: unload unload_order_number_fkey; Type: FK CONSTRAINT; Schema: mes; Owner: postgres
--

ALTER TABLE ONLY mes.unload
    ADD CONSTRAINT unload_order_number_fkey FOREIGN KEY (order_number) REFERENCES mes."order"(number);


--
-- PostgreSQL database dump complete
--

