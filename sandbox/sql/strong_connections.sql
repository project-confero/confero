-- Generate a list of strong connections between candidates

SELECT s_can.name, s_can.party, t_can.name, t_can.party, c.score
FROM (
  SELECT s_com.candidate_id as s_can_id, t_com.candidate_id as t_can_id, SUM(con.score) AS score
  FROM connection AS con
  LEFT JOIN committee AS s_com ON con.source_committee_id = s_com.committee_id
  LEFT JOIN committee AS t_com ON con.target_committee_id = t_com.committee_id
  WHERE s_com.candidate_id IS NOT NULL AND t_com.candidate_id IS NOT NULL
  GROUP BY (s_com.candidate_id, t_com.candidate_id)
) AS c
LEFT JOIN candidate AS s_can ON s_can_id = s_can.id
LEFT JOIN candidate AS t_can ON t_can_id = t_can.id
ORDER BY score DESC
LIMIT 100;
