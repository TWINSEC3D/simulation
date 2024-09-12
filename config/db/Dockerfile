FROM postgres:latest
COPY init.sql /docker-entrypoint-initdb.d/10-init.sql
COPY warehouse_dump.csv /docker-entrypoint-initdb.d/warehouse_dump.csv
