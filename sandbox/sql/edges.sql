SELECT source_committee_id AS source, target_committee_id AS target, score
FROM connection
WHERE (
	source_committee_id IN (SELECT committee_id FROM committee)
    OR target_committee_id IN (SELECT committee_id FROM committee)
);

