WITH contributions AS (
  SELECT
    CASE
      WHEN cmte_id = 'C00401224'
      THEN REGEXP_EXTRACT(memo_text, r'(C[0-9]{{8}})')
      ELSE cmte_id END as cmte_id,
    SPLIT(name, ', ')[ORDINAL(1)] as last,
    TRIM(SPLIT(SPLIT(name, ', ')[SAFE_ORDINAL(2)], ' ')[SAFE_ORDINAL(1)], '.')
      as first,
    CASE
      WHEN TRIM(SPLIT(SPLIT(name, ', ')[SAFE_ORDINAL(2)], ' ')[SAFE_ORDINAL(2)], ".")
        IN ('DR', 'MR', 'MS', 'MRS', 'JR', 'SR', 'II', 'III', 'IV', 'JD', 'ESQ', 'MD')
      THEN NULL
      ELSE TRIM(SPLIT(SPLIT(name, ', ')[SAFE_ORDINAL(2)], ' ')[SAFE_ORDINAL(2)], ".")
      END as middle,
    SUBSTR(zip_code,0,5) as zip_code,
    SUM(transaction_amt) as transaction_amount,
  FROM `bigquery-public-data.fec.indiv{year}`
  WHERE entity_tp = 'IND'
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
  FROM `bigquery-public-data.fec.cn{year}`
  JOIN `bigquery-public-data.fec.cm{year}` USING(cand_id)
)

SELECT * EXCEPT (cmte_id)
FROM contributions AS ctr
LEFT JOIN candidates AS cnd USING(cmte_id)
WHERE cnd.id IS NOT NULL
;
