SELECT COUNT(*)
FROM contribution AS con
LEFT JOIN committee AS com ON con.committee_id = com.committee_id
LEFT JOIN candidate AS can ON com.candidate_id = can.id
WHERE can.office = 'P'
AND can.name = 'SANDERS, BERNARD';


SELECT can.name, can.id, com.committee_id 
FROM committee AS com
LEFT JOIN candidate AS can ON com.candidate_id = can.id
WHERE can.office = 'P'
AND can.name ILIKE 'SANDERS, BERNARD';

SELECT COUNT(*)
FROM contribution
WHERE committee_id = 'C00696948'
OR committee_id = 'C00713339'
OR committee_id = 'C00577130';


SELECT SUM(score)
FROM connection 
WHERE target='P60007168';