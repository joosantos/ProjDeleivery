# Use an official PostgreSQL image as the base image
FROM postgres:16

# Create a volume mount point for the database data directory
VOLUME ./data:/var/lib/postgresql/data

# Copy the database dump file and init script into the container
COPY dump_file.sql /docker-entrypoint-initdb.d/
#COPY scriptChown.sh /docker-entrypoint-initdb.d/

# Change ownership of the data directory to the postgres user
#RUN chown -R postgres:postgres /var/lib/postgresql/data

# Set environment variables (if necessary)
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD 123
ENV POSTGRES_DB kapi

# Expose PostgreSQL port (if necessary)
EXPOSE 5432

# Set the user to postgres and run the PostgreSQL server
USER postgres
CMD ["postgres"]

