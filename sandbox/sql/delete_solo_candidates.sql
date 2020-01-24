DELETE FROM fec_candidate
WHERE id NOT IN (
  SELECT source_id
  FROM fec_connection
);