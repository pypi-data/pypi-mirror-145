import os
import pandas as pd
import snowflake.connector
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
from snowflake.connector.pandas_tools import write_pandas


def fetch_data(sql_query):
    """ fetch data from snowflake tables """

    ctx = snowflake.connector.connect(
        user=os.environ['SK_USER'],
        account=os.environ['SK_ACCOUNT'],
        password=os.environ['SK_PASSWORD'],
        role=os.environ['SK_ROLE'],
        warehouse=os.environ['SK_WAREHOUSE'])

    cur = ctx.cursor()
    try:
        cur.execute(sql_query)
        dataframe = cur.fetch_pandas_all()
        dataframe.columns = dataframe.columns.str.lower()
        return dataframe

    except Exception as ex:
        print(ex)

    finally:
        cur.close()
    ctx.close()


def fetch_data_sso(sql_query, email):
    """ fetch data from snowflake tables using SSO auth """
    ctx = snowflake.connector.connect(
        user=email.upper(),
        account=os.environ['SK_ACCOUNT'],
        authenticator='externalbrowser',
        warehouse=os.environ['SK_WAREHOUSE']
    )
    cur = ctx.cursor()
    try:
        cur.execute(sql_query)
        dataframe = cur.fetch_pandas_all()
        dataframe.columns = dataframe.columns.str.lower()
        return dataframe
    except Exception as ex:
        print(ex)
    finally:
        cur.close()
        ctx.close()


def create_table(dataframe, sf_warehouse, sf_database, sf_schema, sf_table_name, overwrite=False):
    """ create table and write data into snowflake """

    # Create Snowflake engine 
    sf_table_name = sf_table_name.lower()

    engine = create_engine(URL(
        user=os.environ['SK_USER'],
        account=os.environ['SK_ACCOUNT'],
        password=os.environ['SK_PASSWORD'],
        role=os.environ['SK_ROLE'],
        warehouse=sf_warehouse,
        database=sf_database,
        schema=sf_schema))

    print('Snowflake engine created')

    overwrite_table = 'fail'
    if overwrite is True:
        overwrite_table = 'replace'

    # Create Snowflake Connection
    with engine.connect() as connection:

        try:
            # Save dataframe locally
            print('Uploading dataset to Snowflake...')
            filename = f"{sf_table_name}.csv"
            file_path = os.path.abspath(filename)
            dataframe.to_csv(file_path, header=False, index=False)

            # Create table in Snowflake
            dataframe.head(0).to_sql(name=sf_table_name, con=connection, if_exists=overwrite_table, index=False)

            # Put file in S3 stage and copy file to table
            connection.execute(f"put file://{file_path}* @%{sf_table_name}")
            connection.execute(f"copy into {sf_table_name}")
            print('Successfully uploaded {} rows into : {}.{}.{}'.format(dataframe.shape[0], sf_database, sf_schema,
                                                                         sf_table_name.upper()))

        except Exception as ex:
            print(ex)

        finally:
            os.remove(file_path)


def write_data(dataframe, sf_warehouse, sf_database, sf_schema, sf_table_name):
    """ upload dataframe to snowflake table"""

    cnx = snowflake.connector.connect(
        user=os.environ['SK_USER'],
        account=os.environ['SK_ACCOUNT'],
        password=os.environ['SK_PASSWORD'],
        role=os.environ['SK_ROLE'],
        warehouse=sf_warehouse,
        database=sf_database,
        schema=sf_schema)

    try:
        print('Uploading dataset to Snowflake...')
        dataframe.columns = dataframe.columns.str.upper()
        success, nchunks, nrows, _ = write_pandas(cnx, dataframe, table_name=sf_table_name, )
        if success:
            print('Successfully uploaded {} rows into : {}.{}.{}'.format(nrows, sf_database, sf_schema,
                                                                         sf_table_name.upper()))

    except Exception as ex:
        print(ex)
