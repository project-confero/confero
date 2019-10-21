-- Generate a list of strong connections between candidates

SELECT 
  s.id AS s_name,
  s.name AS s_name,
  s.party AS s_party,
  s.office AS s_office,
  t.id AS t_name,
  t.name AS t_name,
  t.party AS t_party,
  t.office AS t_office,
  SUM(con.score) AS score
FROM connection AS con
LEFT JOIN candidate AS s ON con.source = s.id
LEFT JOIN candidate AS t ON con.target = t.id
WHERE s.office = 'P' AND t.office = 'P'
-- AND s.name ILIKE '%BIDEN%'
GROUP BY (s.id, t.id)
ORDER BY SUM(score) DESC
LIMIT 100;
