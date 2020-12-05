DECLARE year STRING default '{year}';

CREATE TEMP FUNCTION nameParse(name STRING)
RETURNS STRUCT<first_name STRING, middle_name STRING, last_name STRING, suffix STRING >
LANGUAGE js
OPTIONS (library = 'gs://confero-project/project/nameParser.js')
AS """
  var f = parseFullName(name, 'all', 0);
  this.first_name = f.first.split('.').join("");
  this.middle_name = f.middle.split('.').join("");
  this.last_name = f.last.split('.').join("");
  this.suffix = f.suffix.split('.').join("");
  return this;
""";

CREATE TEMP TABLE contribs AS
SELECT
  CASE
      WHEN cmte_id = 'C00401224'
      THEN REGEXP_EXTRACT(memo_text, r'(C[0-9]{{8}})')
  ELSE cmte_id END as cmte_id,
  nameParse(name).*,
  SUBSTR(zip_code,0,5) as zip_code,
  transaction_amt as transaction_amount
FROM `bigquery-public-data.fec.indiv*`
WHERE
    _TABLE_SUFFIX = year
    AND entity_tp = 'IND'
    AND transaction_tp IN ('15', '15E')
    AND NOT (
        (REGEXP_CONTAINS(memo_text, r'^REFUND')
        OR memo_text = 'CONTRIBUTION TO ACTBLUE')
        AND cmte_id = 'C00401224'
    )
    AND cmte_id IS NOT NULL
;

CREATE OR REPLACE TEMP TABLE fec AS
with
  contributions AS (
    SELECT
      * EXCEPT(transaction_amount),
      SUM(transaction_amount) as transaction_amount
    FROM contribs
    GROUP BY 1, 2, 3, 4, 5, 6
    ORDER BY 2, 3, 4, 5, 6, 1
  ),

  candidates AS (
    SELECT
      cmte_id,
      cand_id as id,
      cand_name as name,
      cand_pty_affiliation as party,
      cand_election_yr as election_year,
      cand_office_st as state,
      cand_office as office,
      cand_office_district as district,
    FROM `bigquery-public-data.fec.cn*` as cn
    JOIN `bigquery-public-data.fec.cm*` as cm USING(cand_id)
    WHERE
      cm._TABLE_SUFFIX = year
      AND cn._TABLE_SUFFIX = year
  )

SELECT * EXCEPT (cmte_id)
FROM contributions AS ctr
LEFT JOIN candidates AS cnd USING(cmte_id)
WHERE cnd.id IS NOT NULL
;

CREATE OR REPLACE TEMP TABLE matches AS
SELECT
  p.id as source_id,
  l.id as target_id,
  ROW_NUMBER() OVER(PARTITION BY p.id, l.id, p.first_name, p.last_name) as p_id,
FROM fec as p
LEFT JOIN commons.names as n on p.first_name = n.full_name
JOIN fec as l
  ON (
    TRIM(UPPER(l.first_name)) = TRIM(UPPER(p.first_name))
    OR TRIM(UPPER(nick_name)) = TRIM(UPPER(l.first_name))
    OR TRIM(UPPER(full_name)) = TRIM(UPPER(l.first_name))
  )
  AND TRIM(UPPER(p.last_name)) = TRIM(UPPER(l.last_name))
  AND (
    TRIM(UPPER(p.middle_name)) = TRIM(UPPER(l.middle_name) )
    OR STARTS_WITH(TRIM(UPPER(l.middle_name)), SUBSTR(TRIM(UPPER(p.middle_name)), 0, 1))
    OR l.middle_name is null
    OR p.middle_name is null
  )
  AND (
    TRIM(UPPER(p.suffix)) = TRIM(UPPER(l.suffix) )
    OR l.middle_name is null
    OR p.middle_name is null
  )
  AND l.zip_code = p.zip_code
WHERE
  p.id != l.id
ORDER BY 1, 3, 2
;
-- create connections
CREATE OR REPLACE TABLE commons.connections_{year} AS
SELECT
  a.source_id,
  a.target_id,
  count(*) as score
FROM matches as a
WHERE
  a.p_id = 1
GROUP BY 1, 2
HAVING score > 2
ORDER BY 3
;

CREATE OR REPLACE TABLE commons.candidates_{year} AS
WITH
  score_total AS (
    SELECT
      source_id as id,
      sum(score) as score,
    FROM commons.connections_{year}
    GROUP BY 1
  ),

  fec_total AS (
    SELECT
      id,
      name,
      office,
      party,
      state,
      district,
      SUM(transaction_amount) as contribution_amount,
      COUNT(*) as contribution_count,
    FROM fec
    GROUP BY 1, 2, 3, 4, 5, 6
  )

SELECT
  id,
  name,
  office,
  party,
  state,
  district,
  contribution_count,
  contribution_amount,
  score,
FROM fec_total
JOIN score_total USING(id)
ORDER BY score DESC
;

EXPORT DATA OPTIONS(
  uri='gs://confero-data/data/20{year}/connections-*.json',
  format='CSV',
  field_delimiter=',',
  overwrite=true) AS
SELECT * FROM commons.connections_{year};

EXPORT DATA OPTIONS(
  uri='gs://confero-data/data/20{year}/candidates-*.json',
  format='CSV',
  field_delimiter=',',
  overwrite=true) AS
SELECT * FROM commons.candidates_{year};

DROP TABLE commons.connections_{year};
DROP TABLE commons.candidates_{year};
