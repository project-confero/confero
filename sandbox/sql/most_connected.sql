SELECT fec_candidate.id, fec_candidate.name, SUM(score) FROM fec_connection
LEFT JOIN fec_candidate ON fec_connection.source_id = fec_candidate.id
WHERE fec_candidate.office = 'P'
GROUP BY fec_candidate.id
ORDER BY SUM(score) DESC;
