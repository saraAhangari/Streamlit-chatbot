--
-- PostgreSQL database stagedb
--

-- Dumped from database version 15.4 (Debian 15.4-1.pgdg120+1)
-- Dumped by pg_dump version 15.4 (Debian 15.4-1.pgdg120+1)


ALTER DATABASE STAGEDB OWNER TO ADMIN;

SET statement_timeout = 0;

SET lock_timeout = 0;

SET idle_in_transaction_session_timeout = 0;

SET client_encoding = 'UTF8';

SET standard_conforming_strings = on;

SELECT
    PG_CATALOG.SET_CONFIG('search_path',
    'staging',
    FALSE);

SET check_function_bodies = false;

SET xmloption = content;

SET client_min_messages = warning;

SET row_security = off;

--
-- Name: task; Type: SCHEMA; Schema: -; Owner: admin
--

CREATE SCHEMA STAGING;

ALTER SCHEMA STAGING OWNER TO ADMIN;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- COPY tables from source to stage db
--

CREATE TABLE STAGING.ALL_TRANSACTIONS (
    ID INTEGER,
    AMOUNT INTEGER,
    TRANSACTION_DATE TIMESTAMP WITHOUT TIME ZONE,
    TYPE_NAME CHARACTER VARYING(50),
    ACCOUNT_NUMBER INTEGER,
    CUSTOMER_NAME CHARACTER VARYING(255),
    DESTINATION_ACCOUNT_NUMBER INTEGER,
    DESTINATION_CUSTOMER_NAME CHARACTER VARYING(255),
    DESTINATION_ACCOUNT_TYPE_NAME CHARACTER VARYING(50),
    CREDIT BOOLEAN,
    IS_JURIDICAL BOOLEAN
);

ALTER TABLE STAGING.ALL_TRANSACTIONS OWNER TO ADMIN;

CREATE EXTENSION POSTGRES_FDW;

CREATE SERVER DB
FOREIGN DATA WRAPPER POSTGRES_FDW
OPTIONS (HOST 'db', DBNAME 'postgres', PORT '5432');

CREATE USER MAPPING FOR POSTGRES
SERVER DB
OPTIONS (USER 'postgres', PASSWORD 'comeng2002');

IMPORT FOREIGN SCHEMA TASK
FROM SERVER DB
INTO STAGING;