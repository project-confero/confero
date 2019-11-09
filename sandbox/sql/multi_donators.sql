-- How many cross-donors are there?

SELECT COUNT (*) FROM (
SELECT DISTINCT
  source.name,
  source.zip,
  source.employer,
  source.occupation,
  source.committee_id,
  target.committee_id
FROM fec_contribution AS source
LEFT JOIN fec_contribution AS target
ON (
  source.name = target.name
  AND source.zip = target.zip
  AND source.employer = target.employer
  AND source.occupation = target.occupation
)
-- Single doners don't count
WHERE target.committee_id IS NOT NULL
-- Skip un-matchable people
AND source.employer IS NOT NULL
AND source.occupation IS NOT NULL
AND target.employer IS NOT NULL
AND target.occupation IS NOT NULL
-- Skip self-matches
AND source.committee_id != target.committee_id
) as c;