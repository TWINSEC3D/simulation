-- Create table for transport units
CREATE TABLE IF NOT EXISTS public.transport_units (
    id varchar NULL,
    color varchar NULL,
    "type" varchar NULL,
    weight int4 NULL,
    height int4 NULL,
    length int4 NULL,
    width int4 NULL,
    current_loc varchar NULL,
    outbound_request bool NULL
);

-- Create table for warehouse occupancy
CREATE TABLE IF NOT EXISTS public.warehouse (
    y int4 NULL,
    x int4 NULL,
    direction varchar NULL,
    seat_id varchar NULL,
    status varchar NULL
);

-- Create table for DoS attacker
CREATE TABLE IF NOT EXISTS public.dos_table (
    column1 varchar NULL
);

-- Load data into the warehouse table
COPY public.warehouse (y, x, direction, seat_id, status)
FROM '/docker-entrypoint-initdb.d/warehouse_dump.csv'
DELIMITER ','
CSV HEADER;

-- Create a table to indicate initialization completion
CREATE TABLE IF NOT EXISTS public.init_status (
    status boolean
);

-- Insert a record indicating initialization is complete
INSERT INTO public.init_status (status) VALUES (TRUE);
