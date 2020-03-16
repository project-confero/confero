SELECT
  cand_id as id,
  cand_name as name,
  cand_pty_affiliation as party,
  cand_election_yr as election_year,
  cand_office_st as state,
  cand_office as office,
  cand_office_district as district,
  cand_ici as incumbent_challenger_status,
  cand_status as status,
  cand_pcc as principal_committee_id,
  cand_st1 as address_state_1,
  cand_st2 as address_state_2,
  cand_city as address_city,
  cand_st as address_state,
  cand_zip address_zip
FROM `bigquery-public-data.fec.cn20`;
