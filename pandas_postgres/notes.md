# Notes on ingesting csv data into Postgres with Pandas and Docker

## Run postgres in a Docker container
```
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="grain" \
    -v /c/Users/dataengineer/data:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:13
```
## Connect to the postgres DB with pgcli
`winpty pgcli -h localhost -u root -d grain`
```
Server: PostgreSQL 13.9 (Debian 13.9-1.pgdg110+1)
Version: 3.4.1
Home: http://pgcli.com
root@localhost:grain> \dt
+--------+------+------+-------+
| Schema | Name | Type | Owner |
|--------+------+------+-------|
+--------+------+------+-------+
SELECT 0
Time: 0.016s
root@localhost:grain>
```
## Wget a csv and open it with Pandas
`jupyter notebook Read_Grain.ipynb`

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