#!/bin/sh

# Set the PostgreSQL password as an environment variable
export PGPASSWORD="docker"


# Wait for the init script to complete
until psql -h "postgres" -U "postgres" -d "warehouse" -c "SELECT * FROM public.init_status WHERE status = TRUE;" > /dev/null 2>&1; do
  echo "Waiting for database initialization to complete..."
  sleep 2
done

sleep 20
echo "Database initialization complete. Starting the service."
# You can start your main service here, e.g., by executing another command or script
# exec your-main-service-command
