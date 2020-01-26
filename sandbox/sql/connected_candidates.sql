SELECT can.id, name, office, party, state, district, score, contribution_count, contribution_amount
FROM fec_candidate AS can
INNER JOIN (
  SELECT can.id, SUM(score) AS score
  FROM fec_candidate as can
  INNER JOIN fec_connection as con ON con.source_id = can.id
  GROUP BY can.id
) AS can_score ON can_score.id = can.id
INNER JOIN (
  SELECT 
    can.id,
    SUM(con.transaction_amount) AS contribution_amount,
    COUNT(*) AS contribution_count
  FROM fec_candidate AS can
  LEFT JOIN fec_committee AS com ON com.candidate_id = can.id
  LEFT JOIN fec_contribution AS con ON con.committee_id = com.committee_id
  GROUP BY can.id
) AS can_cont ON can_cont.id = can.id
ORDER BY contribution_amount DESC;
