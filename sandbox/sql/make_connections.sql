-- Create a connection table with the connections between candidates
CREATE TABLE connection AS
SELECT source_committee_id, target_committee_id, COUNT(*) AS score
FROM (
  SELECT DISTINCT
    source.name,
    source.zip,
    source.committee_id AS source_committee_id,
    target.committee_id AS target_committee_id
  FROM contribution AS source
  LEFT JOIN contribution AS target
  ON (
    source.name = target.name
    AND source.zip = target.zip
    AND source.employer = target.employer
    AND source.occupation = target.occupation
  )
  WHERE source.committee_id != target.committee_id
  AND source.committee_id != 'C00401224'
  AND target.committee_id != 'C00401224'
  AND source.committee_id IS NOT NULL
  AND target.committee_id IS NOT NULL
) AS shared_contributors
GROUP BY (source_committee_id, target_committee_id);

