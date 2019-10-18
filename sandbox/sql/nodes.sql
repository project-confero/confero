SELECT 
DISTINCT ON (com.committee_id)
com.committee_id AS id, candidate_name, party, candidate_office
FROM committee AS com
LEFT JOIN candidates AS can ON can.id = com.candidate_id
WHERE (
  com.committee_id IN (SELECT target_committee_id FROM connections)
  OR com.committee_id IN (SELECT source_committee_id FROM connections)
);

