-- A list of people with the same name and zip, but different occupations. Many of these are probably matches.

SELECT DISTINCT
  source.name,
  source.zip,
  source.employer,
  source.occupation,
  target.employer,
  target.occupation
FROM fec_contribution AS source
LEFT JOIN fec_contribution AS target
ON (
  source.name = target.name
  AND source.zip = target.zip
  AND (
    source.employer != target.employer
    OR source.occupation != target.occupation
  )
)
-- Single doners don't count
WHERE target.committee_id IS NOT NULL
AND source.employer IS NOT NULL
AND source.occupation IS NOT NULL
AND target.employer IS NOT NULL
AND target.occupation IS NOT NULL;
