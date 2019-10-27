SELECT DISTINCT can.id, can.name, can.party, can.office
FROM connection AS conn
LEFT JOIN candidate AS can ON conn.source = can.id
