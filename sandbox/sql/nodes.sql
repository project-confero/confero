SELECT 
DISTINCT ON (com.committee_id)
com.committee_id AS id, can.name, party, can.office
FROM committee AS com
LEFT JOIN candidate AS can ON can.id = com.candidate_id
WHERE (
  com.committee_id IN (SELECT target_committee_id FROM connection)
  OR com.committee_id IN (SELECT source_committee_id FROM connection)
);

