SELECT
    cmte_id as id,
    cmte_id as committee_id,
    cand_id as candidate_id,
    cmte_tp as committee_type,
    cmte_dsgn as committee_designation
FROM `bigquery-public-data.fec.cm20`;
