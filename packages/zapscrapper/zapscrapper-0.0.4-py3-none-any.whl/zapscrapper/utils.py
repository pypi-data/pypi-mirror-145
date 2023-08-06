import pandas as pd
import os

import boto3

from urllib.parse import quote_plus  # PY2: from urllib import quote_plus
from sqlalchemy.engine import create_engine

from os.path import join


def file_print(
    content: str,
    file: str,
    mode: str = "write",
    sep: str = " ",
    end: str = "\n",
    **kwargs,
) -> None:
    """Print the content to file

    :param content: Content to be printed
    :type content: str
    :param file: Path to the file
    :type file: str
    :param mode: Write mode. Can be 'write' or 'append', defaults to 'write'
    :type mode: str, optional
    :param sep: string inserted between values, defaults to
    :type sep: str, optional
    :param end: string appended after the last value, defaults to '\n'
    :type end: str, optional
    """
    if mode == "write":
        mode = "w"
    elif mode == "append":
        mode = "a"

    with open(file, mode) as text_file:
        print(content, file=text_file, sep=sep, end=end, **kwargs)


def athena_format(input, output):

    df_ctr = pd.read_csv(input)

    try:
        df_ctr = df_ctr.drop(columns="Unnamed: 0")
    except:
        pass

    json_input = input.replace(".csv", ".json")

    df_ctr.to_json(json_input, orient="records")

    file = open(json_input)
    string = file.read().replace("\n", " ")
    file.close()

    string = string.replace("},", "}\n")
    string = string.replace("[{", "{")
    string = string.replace("}]", "}")

    file_print(string, file=output)


def remove_file(file):

    if os.path.exists(file):
        os.remove(file)
    else:
        print("The file does not exist")


def make_directory(path):
    """Creates a dict if it does not exists.

    :param path: path of new directory
    :type path: str
    """
    if not os.path.exists(path):
        os.makedirs(path)


def upload_dataframe_to_s3(
    data,
    filename,
    aws_access_key_id=None,
    aws_secret_access_key=None,
    bucket=None,
    s3_path=None,
):
    csv_file = filename + ".csv"
    json_file = filename + ".json"

    data = data.reset_index()

    if "index" in data.columns:
        data.drop(columns=["index"])

    data.to_csv(csv_file)

    athena_format(csv_file, json_file)

    s3 = boto3.resource(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    try:
        s3.meta.client.upload_file(json_file, bucket, join(s3_path, json_file))

    except Exception as exp:
        print("[error]: ", exp)

    remove_file(csv_file)
    remove_file(json_file)


def athena_query(
    query,
    aws_access_key_id,
    aws_secret_access_key,
    region_name,
    schema_name,
    bucket,
    s3_staging_dir,
):

    try:
        conn_str = (
            "awsathena+rest://{aws_access_key_id}:{aws_secret_access_key}@athena.{region_name}.amazonaws.com:443/"
            "{schema_name}?s3_staging_dir={s3_staging_dir}"
        )
        engine = create_engine(
            conn_str.format(
                aws_access_key_id=quote_plus(aws_access_key_id),
                aws_secret_access_key=quote_plus(aws_secret_access_key),
                region_name=region_name,
                schema_name=schema_name,
                s3_staging_dir=quote_plus("s3://" + bucket + "/" + s3_staging_dir),
            )
        )
    except Exception as err:
        print("[error]", err)

    try:
        conn = engine.connect()
        df = pd.read_sql_query(query, conn)
        conn.close()

    except Exception as err:
        df = None
        print("[error]", err)

    try:
        clear_temp(aws_access_key_id, aws_secret_access_key, bucket, s3_staging_dir)
    except Exception as err:
        print("[error]", err)

    return df


# Deletes all files in your path so use carefully!
def clear_temp(aws_access_key_id, aws_secret_access_key, bucket, s3_staging_dir):
    s3 = boto3.resource(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    my_bucket = s3.Bucket(bucket)
    for item in my_bucket.objects.filter(Prefix=s3_staging_dir):
        if s3_staging_dir in item.key:
            item.delete()


def athena_col_type(col):
    if col.dtype.name == "object":
        return "string"
    elif col.dtype.name == "float64":
        return "double"
    elif col.dtype.name == "float":
        return "double"
    elif col.dtype.name == "int64":
        return "integer"
    elif col.dtype.name == "int":
        return "integer"


def generate_creation_query(df, table_name):

    create_query = f"CREATE EXTERNAL TABLE {table_name}(\n"

    for col in df:
        create_query = (
            create_query + "  " + col + " " + athena_col_type(df[col]) + ",\n"
        )

    create_query = create_query[:-2]

    create_query = create_query + (
        ")\n"
        "ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'\n"
        f"LOCATION 's3://emdemor-athena/data/{table_name}/'\n"
    )
    return create_query
