DROP TABLE IF EXISTS candidate;
DROP TABLE IF EXISTS committee;
DROP TABLE IF EXISTS connection;
DROP TABLE IF EXISTS contribution;

CREATE TABLE candidate (
    id character varying(10) NOT NULL,
    name character varying(200),
    party character varying(3),
    office character varying(1),
    state character varying(2),
    district character varying(2)
);

CREATE TABLE committee (
    candidate_id character varying(9) NOT NULL,
    committee_id character varying(9) NOT NULL
);

CREATE TABLE connection (
    source character varying(9),
    target character varying(9),
    score bigint
);

CREATE TABLE contribution (
    id numeric(19,0) NOT NULL,
    committee_id character varying(9),
    name character varying(200),
    zip character varying(9),
    employer character varying(38),
    occupation character varying(38)
);


ALTER TABLE ONLY candidate
    ADD CONSTRAINT campaigns_pkey PRIMARY KEY (id);

CREATE INDEX contributor
ON contribution(name, zip, employer, occupation);
