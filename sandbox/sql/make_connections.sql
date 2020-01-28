-- populates the connection table with the connections between candidates
INSERT INTO fec_connection (source_id, target_id, score)
SELECT s_com.candidate_id AS source, t_com.candidate_id AS target, SUM(con.score) AS score
FROM (
  SELECT source_committee_id, target_committee_id, COUNT(*) AS score
  FROM (
    SELECT DISTINCT
      source.name,
      source.zip,
      source.employer,
      source.occupation,
      source.committee_id AS source_committee_id,
      target.committee_id AS target_committee_id
    FROM fec_contribution AS source
    INNER JOIN fec_contribution AS target
    ON (
      source.name = target.name
      AND source.zip = target.zip
      AND source.employer = target.employer
      AND (
        source.occupation = target.occupation 
        OR (source.occupation IS NULL 
        AND target.occupation IS NULL)
      )
    )
    WHERE source.committee_id != target.committee_id
    AND source.committee_id != 'C00401224'
    AND target.committee_id != 'C00401224'
    AND source.committee_id IS NOT NULL
    AND target.committee_id IS NOT NULL
  ) AS shared_contributors
  GROUP BY (source_committee_id, target_committee_id)
) as con
INNER JOIN fec_committee AS s_com ON con.source_committee_id = s_com.committee_id
INNER JOIN fec_committee AS t_com ON con.target_committee_id = t_com.committee_id
WHERE s_com.candidate_id IS NOT NULL AND t_com.candidate_id IS NOT NULL
GROUP BY (s_com.candidate_id, t_com.candidate_id)
HAVING SUM(con.score) > 2
ORDER BY score DESC;