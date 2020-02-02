SELECT 
  e.party,
  1.0 * extraparty / interparty AS ratio
FROM (
  SELECT source.party, SUM(score) AS interparty
  FROM fec_connection AS conn
  INNER JOIN fec_candidate AS source ON source.id = conn.source_id
  INNER JOIN fec_candidate AS target ON target.id = conn.target_id
  WHERE target.party = source.party
  GROUP BY source.party
) AS i
FULL OUTER JOIN (
  SELECT source.party, SUM(score) AS extraparty
  FROM fec_connection AS conn
  INNER JOIN fec_candidate AS source ON source.id = conn.source_id
  INNER JOIN fec_candidate AS target ON target.id = conn.target_id
  WHERE target.party != source.party
  GROUP BY source.party
) AS e ON i.party = e.party
ORDER BY extraparty DESC;
