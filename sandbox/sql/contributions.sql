SELECT
  CASE
    WHEN cmte_id = 'C00401224'
    THEN REGEXP_EXTRACT(memo_text, r'(C[0-9]{8})')
    ELSE cmte_id END as committee_id,
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
FROM `bigquery-public-data.fec.indiv20`
WHERE entity_tp = 'IND'
    AND transaction_tp IN ('15', '15E')
    AND NOT (
        (REGEXP_CONTAINS(memo_text, r'^REFUND')
          OR memo_text = 'CONTRIBUTION TO ACTBLUE')
        AND cmte_id = 'C00401224'
    )
GROUP BY 1, 2, 3, 4, 5
ORDER BY 2, 3, 4, 5, 1;
