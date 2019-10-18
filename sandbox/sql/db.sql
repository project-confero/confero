--
-- PostgreSQL database dump
--

-- Dumped from database version 11.2
-- Dumped by pg_dump version 11.5

-- Started on 2019-10-17 16:53:28 PDT

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

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 197 (class 1259 OID 5155350)
-- Name: candidates; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.candidate (
    id character varying(10) NOT NULL,
    name character varying(200),
    party character varying(3),
    office character varying(1),
    state character varying(2),
    district character varying(2)
);


ALTER TABLE public.candidate OWNER TO postgres;

--
-- TOC entry 198 (class 1259 OID 5155360)
-- Name: committee; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.committee (
    candidate_id character varying(9) NOT NULL,
    committee_id character varying(9) NOT NULL
);


ALTER TABLE public.committee OWNER TO postgres;

--
-- TOC entry 199 (class 1259 OID 5155387)
-- Name: connection; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.connection (
    source_committee_id character varying(9),
    target_committee_id character varying(9),
    score bigint
);


ALTER TABLE public.connection OWNER TO postgres;

--
-- TOC entry 196 (class 1259 OID 5155347)
-- Name: contribution; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contribution (
    committee_id character varying(9),
    name character varying(200),
    zip character varying(9),
    id numeric(19,0) NOT NULL,
    employer character varying(38),
    occupation character varying(38)
);


ALTER TABLE public.contribution OWNER TO postgres;

--
-- TOC entry 3051 (class 2606 OID 5155354)
-- Name: candidates campaigns_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.candidate
    ADD CONSTRAINT campaigns_pkey PRIMARY KEY (id);


--
-- TOC entry 3049 (class 2606 OID 5155372)
-- Name: contributions contributions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contribution
    ADD CONSTRAINT contributions_pkey PRIMARY KEY (id);


-- Completed on 2019-10-17 16:53:28 PDT

--
-- PostgreSQL database dump complete
--

