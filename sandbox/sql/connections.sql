SELECT s_com.candidate_id AS source, t_com.candidate_id AS target, SUM(con.score) AS score
FROM connection AS con
INNER JOIN committee AS s_com ON con.source_committee_id = s_com.committee_id
INNER JOIN committee AS t_com ON con.target_committee_id = t_com.committee_id
WHERE s_com.candidate_id IS NOT NULL AND t_com.candidate_id IS NOT NULL
GROUP BY (s_com.candidate_id, t_com.candidate_id)
ORDER BY score DESC
