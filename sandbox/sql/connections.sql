-- Create a connections table with the connections between candidates
CREATE TABLE connections AS
SELECT source_committee_id, target_committee_id, COUNT(*) AS score
FROM (
  SELECT DISTINCT
    source.contributor_name,
    source.zip,
    source.committee_id AS source_committee_id,
    target.committee_id AS target_committee_id
  FROM contributions AS source
  LEFT JOIN contributions AS target
  ON (
    source.contributor_name = target.contributor_name
    AND source.zip = target.zip
  )
  WHERE source.committee_id != target.committee_id
  AND source.committee_id != 'C00401224'
  AND target.committee_id != 'C00401224'
  AND source.committee_id IS NOT NULL
  AND target.committee_id IS NOT NULL
) AS shared_contributors
GROUP BY (source_committee_id, target_committee_id);

