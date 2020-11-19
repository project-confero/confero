DECLARE year STRING DEFAULT '20';

-- create temp clean fec table
CREATE OR REPLACE TEMP TABLE fec AS
  WITH contributions AS (
    SELECT
      CASE
        WHEN cmte_id = 'C00401224'
        THEN REGEXP_EXTRACT(memo_text, r'(C[0-9]{{8}})')
        ELSE cmte_id END as cmte_id,
      SPLIT(name, ', ')[ORDINAL(1)] as last_name,
      TRIM(SPLIT(SPLIT(name, ', ')[SAFE_ORDINAL(2)], ' ')[SAFE_ORDINAL(1)], '.')
        as first_name,
      CASE
        WHEN TRIM(SPLIT(SPLIT(name, ', ')[SAFE_ORDINAL(2)], ' ')[SAFE_ORDINAL(2)], ".")
          IN ('DR', 'MR', 'MS', 'MRS', 'JR', 'SR', 'II', 'III', 'IV', 'JD', 'ESQ', 'MD')
        THEN NULL
        ELSE TRIM(SPLIT(SPLIT(name, ', ')[SAFE_ORDINAL(2)], ' ')[SAFE_ORDINAL(2)], ".")
        END as middle_name,
      SUBSTR(zip_code,0,5) as zip_code,
      SUM(transaction_amt) as transaction_amount,
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
    GROUP BY 1, 2, 3, 4, 5
    ORDER BY 2, 3, 4, 5, 1
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

WITH matches as (
  SELECT 
    p.id as source_id,
    l.id as target_id,
    ROW_NUMBER() OVER(PARTITION BY p.id, l.id, p.first_name, p.last_name) as p_id,
  FROM fec as p
  LEFT JOIN `confero-271219.commons.names` as n on p.first_name = n.full_name
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
    AND l.zip_code = p.zip_code
    WHERE 
      p.id != l.id
    ORDER BY 1, 3, 2
)
