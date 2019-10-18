-- Generate a list of strong connections between candidates

SELECT s_can.candidate_name, s_can.party, t_can.candidate_name, t_can.party, con.score
FROM connections AS con
LEFT JOIN committee AS s_com ON con.source_committee_id = s_com.committee_id
LEFT JOIN committee AS t_com ON con.target_committee_id = t_com.committee_id
LEFT JOIN candidates AS s_can ON s_com.candidate_id = s_can.id
LEFT JOIN candidates AS t_can ON t_com.candidate_id = t_can.id
WHERE s_com.candidate_id IS NOT NULL AND t_com.candidate_id IS NOT NULL
ORDER BY score DESC
LIMIT 100;
