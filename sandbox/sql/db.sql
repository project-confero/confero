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

CREATE TABLE public.candidates (
    id character varying(9) NOT NULL,
    candidate_name character varying(200),
    party character varying(3),
    candidate_office character varying(1),
    committee_id character varying(9)
);


ALTER TABLE public.candidates OWNER TO postgres;

--
-- TOC entry 198 (class 1259 OID 5155360)
-- Name: committee; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.committee (
    candidate_id character varying(9) NOT NULL,
    committee_id character varying(9) NOT NULL,
    id numeric NOT NULL
);


ALTER TABLE public.committee OWNER TO postgres;

--
-- TOC entry 199 (class 1259 OID 5155387)
-- Name: connections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.connections (
    source_committee_id character varying(9),
    target_committee_id character varying(9),
    score bigint
);


ALTER TABLE public.connections OWNER TO postgres;

--
-- TOC entry 196 (class 1259 OID 5155347)
-- Name: contributions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contributions (
    committee_id character varying(9),
    contributor_name character varying(200),
    zip character varying(9),
    id numeric(19,0) NOT NULL
);


ALTER TABLE public.contributions OWNER TO postgres;

--
-- TOC entry 3051 (class 2606 OID 5155354)
-- Name: candidates campaigns_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.candidates
    ADD CONSTRAINT campaigns_pkey PRIMARY KEY (id);


--
-- TOC entry 3053 (class 2606 OID 5155370)
-- Name: committee committee_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.committee
    ADD CONSTRAINT committee_pkey PRIMARY KEY (id);


--
-- TOC entry 3049 (class 2606 OID 5155372)
-- Name: contributions contributions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contributions
    ADD CONSTRAINT contributions_pkey PRIMARY KEY (id);


-- Completed on 2019-10-17 16:53:28 PDT

--
-- PostgreSQL database dump complete
--

