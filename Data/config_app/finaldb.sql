--
-- PostgreSQL database finaldb
--

-- Dumped from database version 15.4 (Debian 15.4-1.pgdg120+1)
-- Dumped by pg_dump version 15.4 (Debian 15.4-1.pgdg120+1)



ALTER DATABASE FINALDB OWNER TO ADMIN;

SET statement_timeout = 0;

SET lock_timeout = 0;

SET idle_in_transaction_session_timeout = 0;

SET client_encoding = 'UTF8';

SET standard_conforming_strings = on;

SELECT
    PG_CATALOG.SET_CONFIG('search_path',
    '',
    FALSE);

SET check_function_bodies = false;

SET xmloption = content;

SET client_min_messages = warning;

SET row_security = off;

--
-- Name: staging; Type: SCHEMA; Schema: -; Owner: admin
--

CREATE SCHEMA FACTS;

ALTER SCHEMA FACTS OWNER TO ADMIN;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: transaction_fact Type: TABLE; Schema: staging; Owner: admin
--

CREATE TABLE FACTS.TRANSACTION_FACT (
    ID INTEGER,
    AMOUNT INTEGER,
    TRANSACTION_DATE TIMESTAMP WITHOUT TIME ZONE,
    ACCOUNT_NUMBER INTEGER,
    CUSTOMER_NAME CHARACTER VARYING(255),
    DESTINATION_ACCOUNT_NUMBER INTEGER,
    DESTINATION_CUSTOMER_NAME CHARACTER VARYING(255),
    DESTINATION_ACCOUNT_TYPE_NAME CHARACTER VARYING(50),
    CREDIT BOOLEAN,
    IS_JURIDICAL BOOLEAN
);

ALTER TABLE FACTS.TRANSACTION_FACT OWNER TO ADMIN;

CREATE TABLE FACTS.TURNOVER_PER_ACCOUNT_TYPE (
    ACCOUNT_TYPE_NAME CHARACTER VARYING(50),
    TURNOVER INTEGER,
    TRANSACTION_DATE TIMESTAMP WITHOUT TIME ZONE
);

ALTER TABLE FACTS.TURNOVER_PER_ACCOUNT_TYPE OWNER TO ADMIN;

CREATE TABLE FACTS.ACCOUNT_TURNOVER (
    CUSTOMER_NAME CHARACTER VARYING(50),
    ACCOUNT_NO INTEGER NOT NULL,
    TURNOVER INTEGER,
    TRANSACTION_DATE TIMESTAMP WITHOUT TIME ZONE
);

ALTER TABLE FACTS.ACCOUNT_TURNOVER OWNER TO ADMIN;

-- COPY staging.all_transactions (id, amount, transaction_date, type_name, account_number, customer_name, destination_account_number, destination_customer_name, destination_account_type_name, credit, is_juridical) FROM stdin;
-- 1	540000	2021-03-19 12:29:54	کارت به کارت	10022	علی محمدی	30035	عباس علوی	قرض الحسنه	f	f
-- 2	60500000	2021-06-23 13:30:46	کارت به کارت	10022	علی محمدی	20021	محمد علی پور	سپرده کوتاه مدت	t	f
-- 3	520000000	2021-07-02 22:31:27	پایا	20021	محمد علی پور	10032	علی محمدی	قرض الحسنه	t	f
-- 4	1272300000	2021-08-02 14:35:11	ساتنا	30035	عباس علوی	40023	شرکت کوچک	سپرده کوتاه مدت	f	t
-- 5	720000	2022-09-07 15:28:51	کارت به کارت	30035	عباس علوی	10032	علی محمدی	قرض الحسنه	f	f
-- 6	8450000	2022-11-09 22:29:53	کارت به کارت	40023	شرکت کوچک	20021	محمد علی پور	سپرده کوتاه مدت	t	f
-- 7	985000	2023-02-27 20:50:50	کارت به کارت	10022	علی محمدی	10032	علی محمدی	قرض الحسنه	t	f
-- 8	1710520750	2023-03-31 23:35:56	ساتنا	40023	شرکت کوچک	30035	عباس علوی	قرض الحسنه	t	f
-- \.