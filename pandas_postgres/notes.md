# Notes on ingesting csv data into Postgres with Pandas and Docker

## Run postgres in a Docker container
```
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="grain" \
    -v /c/Users/dataengineer/grain/data:/var/lib/postgresql/data \
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
[notebook](https://github.com/BrownCasey/data-engineer-tools/blob/main/pandas_postgres/Read_Grain.ipynb)

## Connect to postgres with sqlalchemy
```
from sqlalchemy import create_engine
conn = create_engine("postgresql://root:root@localhost:5432/grain")
conn.connect()
<sqlalchemy.engine.base.Connection at 0x232280332b0>
```

## Create a table and insert data
```
print(pd.io.sql.get_schema(df, con=conn, name="grain_tbl"))

CREATE TABLE grain_tbl (
	"SC_Group_ID" BIGINT, 
	"SC_Group_Desc" TEXT, 
	"SC_GroupCommod_ID" BIGINT, 
	"SC_GroupCommod_Desc" TEXT, 
	"SC_Geography_ID" BIGINT, 
	"SortOrder" FLOAT(53), 
	"SC_GeographyIndented_Desc" TEXT, 
	"SC_Commodity_ID" BIGINT, 
	"SC_Commodity_Desc" TEXT, 
	"SC_Attribute_ID" BIGINT, 
	"SC_Attribute_Desc" TEXT, 
	"SC_Unit_ID" BIGINT, 
	"SC_Unit_Desc" TEXT, 
	"Year_ID" BIGINT, 
	"SC_Frequency_ID" BIGINT, 
	"SC_Frequency_Desc" TEXT, 
	"Timeperiod_ID" BIGINT, 
	"Timeperiod_Desc" TEXT, 
	"Amount" FLOAT(53)
)
```

`df.head(n=0).to_sql(name="grain", con=conn, if_exists='replace')`

## Create a network with Docker
```
$ docker ps -a --filter "name=pg-database"
CONTAINER ID   IMAGE         COMMAND                  CREATED         STATUS         PORTS                    NAMES
7f19f0c8e74c   postgres:13   "docker-entrypoint.s…"   8 minutes ago   Up 8 minutes   0.0.0.0:5432->5432/tcp   pg-database

$ docker rm pg-database
$ docker network ls
$ docker network rm pg-network
$ docker images | grep etl
etl              grain      5d1a90c9d63e   20 hours ago    1.11GB
etl              test       2d92988b0dab   6 days ago      1.09GB
```

```
docker network create pg-network
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="grain" \
    -v /c/Users/dataengineer/grain/data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network \
    --name pg-database \
    postgres:13

docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@example.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name pgadmin \
    dpage/pgadmin4

# open http://localhost:8080
# host=pg-database
```
## Take data arguments in python script
```
import argparse

def main(params):
    p1 = params.param1
    p2 = params.param2
    print(f"Today's weather is {p1} with a chance of {p2}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--param1', help='Description for param1')
    parser.add_argument('--param2', help='Description for param2')

    args = parser.parse_args()
    
    main(args)
```
## Make the Dockerfile and build it
```FROM python:3.9

RUN pip install pandas sqlalchemy wget psycopg2

COPY etl_grain.py etl_grain.py

ENTRYPOINT ["python", "etl_grain.py"]
```

`docker build -f Dockerfile.grain -t etl:grain .`

## Run the import
```
docker run -it \
--network=pg-network \
etl:grain \
--url=https://www.ers.usda.gov/webdocs/DataFiles/50048/FeedGrains.zip \
--auth_u=root \
--auth_p=root \
--host=pg-database \
--port=5432 \
--db=grain
```
```
<sqlalchemy.engine.base.Connection object at 0x7f26e9f7c160>
100% [..........................................................................] 5399829 / 5399829
Inserted 100000 in 6.7 seconds.
Inserted 100000 in 7.2 seconds.
Inserted 100000 in 6.7 seconds.
Inserted 97725 in 6.6 seconds.
Finished inserts
```

```
Server: PostgreSQL 13.9 (Debian 13.9-1.pgdg110+1)
Version: 3.4.1
Home: http://pgcli.com
grain> select count(1) from grain_data;
+--------+
| count  |
|--------|
| 497725 |
+--------+
SELECT 1
Time: 0.040s
```