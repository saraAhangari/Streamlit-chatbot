--
-- PostgreSQL database sourcedb
--
-- Dumped from database version 15.4 (Debian 15.4-1.pgdg120+1)
-- Dumped by pg_dump version 15.4 (Debian 15.4-1.pgdg120+1)



CREATE ROLE ADMIN;

ALTER DATABASE POSTGRES OWNER TO ADMIN;

CREATE SCHEMA IF NOT EXISTS TASK;

ALTER SCHEMA TASK OWNER TO ADMIN;

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
-- Name: account; Type: TABLE; Schema: task; Owner: admin
--

CREATE TABLE TASK.ACCOUNT (
    ID INTEGER NOT NULL,
    CLIENT_ID INTEGER NOT NULL,
    TYPE INTEGER NOT NULL,
    ACCOUNT_NO INTEGER NOT NULL,
    IS_ACTIVE BOOLEAN NOT NULL,
    CREATION_DATE TIMESTAMP WITHOUT TIME ZONE,
    LAST_MODIFICATION_DATE TIMESTAMP WITHOUT TIME ZONE
);

ALTER TABLE TASK.ACCOUNT OWNER TO ADMIN;

--
-- Name: account_types; Type: TABLE; Schema: task; Owner: admin
--

CREATE TABLE TASK.ACCOUNT_TYPES (
    ID INTEGER NOT NULL,
    NAME CHARACTER VARYING(50),
    DESCRIPTION CHARACTER VARYING(255)
);

ALTER TABLE TASK.ACCOUNT_TYPES OWNER TO ADMIN;

--
-- Name: customer; Type: TABLE; Schema: task; Owner: admin
--

CREATE TABLE TASK.CUSTOMER (
    ID INTEGER NOT NULL,
    NAME CHARACTER VARYING(255),
    BIRTH_DATE DATE,
    CUSTOMER_NO INTEGER,
    IS_ACTIVE BOOLEAN,
    CREATION_DATE TIMESTAMP WITHOUT TIME ZONE,
    LAST_MODIFICATION_DATE TIMESTAMP WITHOUT TIME ZONE,
    TYPE INTEGER NOT NULL
);

ALTER TABLE TASK.CUSTOMER OWNER TO ADMIN;

--
-- Name: customer_type; Type: TABLE; Schema: task; Owner: admin
--

CREATE TABLE TASK.CUSTOMER_TYPE (
    ID INTEGER NOT NULL,
    NAME CHARACTER VARYING(50),
    DESCRIPTION CHARACTER VARYING(255)
);

ALTER TABLE TASK.CUSTOMER_TYPE OWNER TO ADMIN;

--
-- Name: smaple; Type: TABLE; Schema: task; Owner: admin
--

CREATE TABLE TASK.SMAPLE (
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

ALTER TABLE TASK.SMAPLE OWNER TO ADMIN;

--
-- Name: transaction; Type: TABLE; Schema: task; Owner: admin
--

CREATE TABLE TASK.TRANSACTION (
    ID INTEGER NOT NULL,
    AMOUNT INTEGER NOT NULL,
    TRANSACTION_DATE TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    TYPE INTEGER NOT NULL,
    FROM_ACCOUNT_ID INTEGER NOT NULL,
    TO_ACCOUNT_ID INTEGER NOT NULL,
    CREDIT BOOLEAN NOT NULL
);

ALTER TABLE TASK.TRANSACTION OWNER TO ADMIN;

--
-- Name: transaction_type; Type: TABLE; Schema: task; Owner: admin
--

CREATE TABLE TASK.TRANSACTION_TYPE (
    ID INTEGER NOT NULL,
    NAME CHARACTER VARYING(50),
    DESCRIPTION CHARACTER VARYING(255)
);

ALTER TABLE TASK.TRANSACTION_TYPE OWNER TO ADMIN;

-- --
-- -- Data for Name: account; Type: TABLE DATA; Schema: task; Owner: admin
-- --

-- COPY task.account (id, client_id, type, account_no, is_active, creation_date, last_modification_date) FROM stdin;
-- 1	1	1	10022	t	2021-07-08 21:23:06	2022-09-02 21:23:16
-- 2	1	3	10032	t	2020-02-26 14:24:02	2022-03-01 11:24:14
-- 3	2	1	20021	t	2022-03-18 23:24:56	2023-01-07 02:25:06
-- 4	2	2	20041	f	2021-08-05 13:25:43	2022-06-03 21:25:54
-- 5	3	3	30035	t	2022-09-05 14:26:39	2023-08-16 19:26:50
-- 6	4	1	40023	t	2021-02-06 21:27:57	2022-08-11 22:28:06
-- 7	5	3	50031	f	2021-03-29 19:28:43	2021-12-27 22:28:56
-- \.


-- --
-- -- Data for Name: account_types; Type: TABLE DATA; Schema: task; Owner: admin
-- --

-- COPY task.account_types (id, name, description) FROM stdin;
-- 1	سپرده کوتاه مدت	سپرده پس انداز کوتاه مدت
-- 2	سپرده بلند مدت	سپرده پس انداز بلند مدت
-- 3	قرض الحسنه	حساب پس انداز قرض الحسنه
-- \.


-- --
-- -- Data for Name: customer; Type: TABLE DATA; Schema: task; Owner: admin
-- --

-- COPY task.customer (id, name, birth_date, customer_no, is_active, creation_date, last_modification_date, type) FROM stdin;
-- 1	علی محمدی	1997-11-19	354712	t	2021-05-07 21:15:42	2022-09-06 21:16:03	1
-- 2	محمد علی پور	1981-05-07	354822	t	2021-10-29 12:22:44	2023-11-02 13:56:02	1
-- 3	عباس علوی	2000-11-09	353412	t	2022-12-05 21:19:30	2023-01-05 21:19:42	1
-- 4	شرکت کوچک	\N	100112	t	2023-11-01 16:14:44	2023-11-02 11:22:03	2
-- 5	شرکت بزرگ	\N	100113	f	2020-08-08 06:21:38	2023-11-04 21:21:54	2
-- \.


-- --
-- -- Data for Name: customer_type; Type: TABLE DATA; Schema: task; Owner: admin
-- --

-- COPY task.customer_type (id, name, description) FROM stdin;
-- 1	حقیقی	کاربر حقیقی
-- 2	حقوقی	کاربر حقوقی
-- 3	کودک	کاربران زیر سن قانونی
-- \.


-- --
-- -- Data for Name: smaple; Type: TABLE DATA; Schema: task; Owner: admin
-- --

-- COPY task.smaple (id, amount, transaction_date, type_name, account_number, customer_name, destination_account_number, destination_customer_name, destination_account_type_name, credit, is_juridical) FROM stdin;
-- 1	540000	2021-03-19 12:29:54	کارت به کارت	10022	علی محمدی	30035	عباس علوی	قرض الحسنه	f	f
-- 2	60500000	2021-06-23 13:30:46	کارت به کارت	10022	علی محمدی	20021	محمد علی پور	سپرده کوتاه مدت	t	f
-- 3	520000000	2021-07-02 22:31:27	پایا	20021	محمد علی پور	10032	علی محمدی	قرض الحسنه	t	f
-- 4	1272300000	2021-08-02 14:35:11	ساتنا	30035	عباس علوی	40023	شرکت کوچک	سپرده کوتاه مدت	f	t
-- 5	720000	2022-09-07 15:28:51	کارت به کارت	30035	عباس علوی	10032	علی محمدی	قرض الحسنه	f	f
-- 6	8450000	2022-11-09 22:29:53	کارت به کارت	40023	شرکت کوچک	20021	محمد علی پور	سپرده کوتاه مدت	t	f
-- 7	985000	2023-02-27 20:50:50	کارت به کارت	10022	علی محمدی	10032	علی محمدی	قرض الحسنه	t	f
-- 8	1710520750	2023-03-31 23:35:56	ساتنا	40023	شرکت کوچک	30035	عباس علوی	قرض الحسنه	t	f
-- \.


-- --
-- -- Data for Name: transaction; Type: TABLE DATA; Schema: task; Owner: admin
-- --

-- COPY task.transaction (id, amount, transaction_date, type, from_account_id, to_account_id, credit) FROM stdin;
-- 1	540000	2021-03-19 12:29:54	1	1	5	f
-- 2	60500000	2021-06-23 13:30:46	1	3	1	t
-- 3	520000000	2021-07-02 22:31:27	2	2	3	t
-- 4	1272300000	2021-08-02 14:35:11	3	5	6	f
-- 5	720000	2022-09-07 15:28:51	1	5	2	f
-- 6	8450000	2022-11-09 22:29:53	1	3	6	t
-- 7	985000	2023-02-27 20:50:50	1	2	1	t
-- 8	1710520750	2023-03-31 23:35:56	3	5	6	t
-- \.


-- --
-- -- Data for Name: transaction_type; Type: TABLE DATA; Schema: task; Owner: admin
-- --

-- COPY task.transaction_type (id, name, description) FROM stdin;
-- 1	کارت به کارت	انتقال وجه کارت به کارت
-- 2	پایا	انتقال وجه پایا
-- 3	ساتنا	انتقال وجه ساتنا
-- \.


--
-- Name: account account_pk; Type: CONSTRAINT; Schema: task; Owner: admin
--

ALTER TABLE ONLY TASK.ACCOUNT ADD CONSTRAINT ACCOUNT_PK PRIMARY KEY (ID);

--
-- Name: account_types account_types_pk; Type: CONSTRAINT; Schema: task; Owner: admin
--

ALTER TABLE ONLY TASK.ACCOUNT_TYPES ADD CONSTRAINT ACCOUNT_TYPES_PK PRIMARY KEY (ID);

--
-- Name: customer customer_pk; Type: CONSTRAINT; Schema: task; Owner: admin
--

ALTER TABLE ONLY TASK.CUSTOMER ADD CONSTRAINT CUSTOMER_PK PRIMARY KEY (ID);

--
-- Name: customer_type customer_type_pk; Type: CONSTRAINT; Schema: task; Owner: admin
--

ALTER TABLE ONLY TASK.CUSTOMER_TYPE ADD CONSTRAINT CUSTOMER_TYPE_PK PRIMARY KEY (ID);

--
-- Name: transaction transaction_pk; Type: CONSTRAINT; Schema: task; Owner: admin
--

ALTER TABLE ONLY TASK.TRANSACTION ADD CONSTRAINT TRANSACTION_PK PRIMARY KEY (ID);

--
-- Name: transaction_type transaction_type_pk; Type: CONSTRAINT; Schema: task; Owner: admin
--

ALTER TABLE ONLY TASK.TRANSACTION_TYPE ADD CONSTRAINT TRANSACTION_TYPE_PK PRIMARY KEY (ID);

--
-- Name: account account_account_types_id_fk; Type: FK CONSTRAINT; Schema: task; Owner: admin
--

ALTER TABLE ONLY TASK.ACCOUNT ADD CONSTRAINT ACCOUNT_ACCOUNT_TYPES_ID_FK FOREIGN KEY (TYPE) REFERENCES TASK.ACCOUNT_TYPES(ID);

--
-- Name: account account_customer_id_fk; Type: FK CONSTRAINT; Schema: task; Owner: admin
--

ALTER TABLE ONLY TASK.ACCOUNT ADD CONSTRAINT ACCOUNT_CUSTOMER_ID_FK FOREIGN KEY (CLIENT_ID) REFERENCES TASK.CUSTOMER(ID);

--
-- Name: customer customer_customer_type_id_fk; Type: FK CONSTRAINT; Schema: task; Owner: admin
--

ALTER TABLE ONLY TASK.CUSTOMER ADD CONSTRAINT CUSTOMER_CUSTOMER_TYPE_ID_FK FOREIGN KEY (TYPE) REFERENCES TASK.CUSTOMER_TYPE(ID);

--
-- Name: transaction transaction_account_id_fk; Type: FK CONSTRAINT; Schema: task; Owner: admin
--

ALTER TABLE ONLY TASK.TRANSACTION ADD CONSTRAINT TRANSACTION_ACCOUNT_ID_FK FOREIGN KEY (FROM_ACCOUNT_ID) REFERENCES TASK.ACCOUNT(ID);

--
-- Name: transaction transaction_account_id_fk2; Type: FK CONSTRAINT; Schema: task; Owner: admin
--

ALTER TABLE ONLY TASK.TRANSACTION ADD CONSTRAINT TRANSACTION_ACCOUNT_ID_FK2 FOREIGN KEY (TO_ACCOUNT_ID) REFERENCES TASK.ACCOUNT(ID);

--
-- Name: transaction transaction_transaction_type_id_fk; Type: FK CONSTRAINT; Schema: task; Owner: admin
--

ALTER TABLE ONLY TASK.TRANSACTION ADD CONSTRAINT TRANSACTION_TRANSACTION_TYPE_ID_FK FOREIGN KEY (TYPE) REFERENCES TASK.TRANSACTION_TYPE(ID);

--
-- PostgreSQL database dump complete
--