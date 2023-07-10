import pandas as pd
import argparse, wget, os
from sqlalchemy import create_engine
from time import time

def main(params):
    url = params.url
    auth_u = params.auth_u
    auth_p = params.auth_p
    host = params.host
    port = params.port
    db = params.db

    conn = create_engine(f'postgresql://{auth_u}:{auth_p}@{host}:{port}/{db}')
    print(conn.connect())

    file = wget.download(url)

    df_iter = pd.read_csv(file, iterator=True, chunksize=100000)

    df = next(df_iter)

    df.head(n=0).to_sql(name='grain_data', con=conn, if_exists='replace')
    
    df.to_sql(name='grain_data', con=conn, if_exists='append')

    while True:
        try:
            df = next(df_iter)
            timestart = time()
        except StopIteration:
            print('Finished inserts')
            break

        df.to_sql(name='grain_data', con=conn, if_exists='append')
        timeend = time()
        print(f'Inserted {len(df.index)} in {timeend-timestart:.1f} seconds.')
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--url', help='Url to download')
    parser.add_argument('--auth_u', help='db user')
    parser.add_argument('--auth_p', help='db pass')
    parser.add_argument('--host', help='db host')
    parser.add_argument('--port', help='db port')
    parser.add_argument('--db', help='db name')

    args = parser.parse_args()

    main(args)