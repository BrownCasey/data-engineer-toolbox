# Notes on ingesting csv data into Postgres with Pandas and Docker

## Run postgres in a Docker container

## Connect to the postgres DB with pgcli

## Wget a csv and open it with Pandas

## Connect to postgres with sqlalchemy

## Create a table and insert data

## Create a network with Docker

## Take data arguments in insert script

## Make the Dockerfile and build it
`docker build -f Dockerfile.grain -t etl:grain .`

## Run the import
```
docker run -it \
--network=pg-network \
etl:grain \
--url=https://www.ers.usda.gov/webdocs/DataFiles/50048/FeedGrains.zip
--auth_u=root \
--auth_p=root \
--host=pg-database \
--port=5432 \
--db=grain
```