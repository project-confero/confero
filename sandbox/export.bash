# Calculate connection table
psql -d confero_sandbox < ./sql/make_connections.sql

# Sanity check
psql -d confero_sandbox < ./sql/strong_connections.sql

# Export data for Gephi
psql -d confero_sandbox -A -F"," -P"footer=off" -f ./sql/nodes.sql > nodes.csv
psql -d confero_sandbox -A -F"," -P"footer=off" -f ./sql/edges.sql > edges.csv

# Import to Gephi
# Use the Appearence tab, Color, Partition, Party, set colors
# Data tab, filter by office=P, set all to 25 size
# Use Filters tab, add a filter for attribute is not null candidate name
# Use layout tab to run Force Atlas 2, then Fruchterman Reingold

# Export data for confero

psql -d confero_sandbox -A -F"," -P"footer=off" -f ./sql/connections.sql > connections.csv

# Import into confero
psql -d confero -c "COPY fec_connection FROM '"$PWD/connections.csv"' delimiter ',' csv header;"
