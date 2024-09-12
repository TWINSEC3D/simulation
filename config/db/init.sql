-- Drop existing tables if they exist
DROP TABLE IF EXISTS public.transport_units CASCADE;
DROP TABLE IF EXISTS public.warehouse CASCADE;
DROP TABLE IF EXISTS public.dos_table CASCADE;
DROP TABLE IF EXISTS public.init_status CASCADE;

-- create table for transport units
CREATE TABLE public.transport_units (
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

-- create table for warehouse occupancy
CREATE TABLE public.warehouse (
	y int4 NULL,
	x int4 NULL,
	direction varchar NULL,
	seat_id varchar NULL,
	status varchar NULL
);

-- create table for DoS attacker
CREATE TABLE public.dos_table (
	column1 varchar NULL
);

-- Load data into the warehouse table from CSV
COPY public.warehouse (y, x, direction, seat_id, status)
FROM '/docker-entrypoint-initdb.d/warehouse_dump.csv'
DELIMITER ','
CSV HEADER;

-- Create a table to indicate initialization completion
CREATE TABLE public.init_status (
    status boolean
);

-- Insert a record indicating initialization is complete
INSERT INTO public.init_status (status) VALUES (TRUE);
