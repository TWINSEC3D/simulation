#!/bin/bash
# Remove old data from the tables, keep the structure
psql -U $POSTGRES_USER -d $POSTGRES_DB -f /docker-entrypoint-initdb.d/init.sql

# Call the default entrypoint script to start PostgreSQL
docker-entrypoint.sh postgres
