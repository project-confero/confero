DROP INDEX IF EXISTS fec_contribution_contributor;
DROP TABLE IF EXISTS fec_contribution;
DROP TABLE IF EXISTS fec_connection;
DROP TABLE IF EXISTS fec_committee;
DROP TABLE IF EXISTS fec_candidate;

CREATE TABLE fec_candidate (
    id character varying(200) PRIMARY KEY,
    name character varying(200) NOT NULL,
    office character varying(1),
    party character varying(3),
    state character varying(2),
    district integer
);

CREATE TABLE fec_committee (
    committee_id character varying(9) PRIMARY KEY,
    candidate_id character varying(200) REFERENCES fec_candidate(id)
);

CREATE TABLE fec_connection (
    id SERIAL PRIMARY KEY,
    score integer NOT NULL,
    source_id character varying(200) NOT NULL REFERENCES fec_candidate(id),
    target_id character varying(200) NOT NULL REFERENCES fec_candidate(id)
);

CREATE TABLE fec_contribution (
    id bigint PRIMARY KEY,
    name character varying(200),
    zip character varying(9),
    employer character varying(38),
    occupation character varying(38),
    transaction_amount integer NOT NULL,
    committee_id character varying(9) REFERENCES fec_committee(committee_id)
);

CREATE INDEX fec_contribution_contributor ON fec_contribution (name, zip, employer, occupation);
