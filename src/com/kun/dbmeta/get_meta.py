import pymysql
import json

def extract_table_info(host, username, password,database):
    tables = get_non_system_tables(host, username, password, database)
    print(tables)
    connection = pymysql.connect(host=host,
                                 user=username,
                                 password=password,
                                 database=database,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        for full_name in tables:
            with connection.cursor() as cursor:
                # Extract table ddl
                print(f"SHOW CREATE TABLE {full_name['schema_name']}.{full_name['table_name']}")
                cursor.execute(f"SHOW CREATE TABLE {full_name['schema_name']}.{full_name['table_name']}")
                result = cursor.fetchone()
                table_ddl = result['Create Table']

                # Extract field info from information_schema
                cursor.execute(f"SELECT column_name, column_type, column_comment FROM information_schema.columns WHERE table_schema = '{full_name['schema_name']}' AND table_name = '{full_name['table_name']}'")
                fields = cursor.fetchall()

                # Generate JSON output
                output = []
                for idx, field in enumerate(fields):
                    tb_cols = []
                    tb_cols.append({
                        "column_name": field["column_name"],
                        "column_desc": field["column_comment"],
                        "column_type": field["column_type"]
                    })

                    table_id = "t" + str(idx + 1).zfill(3)

                    table_info = {
                        "jsonb_build_object": {
                            "tables": [
                                {
                                    "tb_cols": tb_cols,
                                    "table_id": table_id,
                                    "row_count": None,
                                    "table_ddl": table_ddl,
                                    "tb_topics": [],
                                    "table_name": full_name['table_name'],
                                    "table_type": "表",
                                    "tb_indexes": None,
                                    "table_schema": "office_operation",
                                    "table_name_ch": "" # Fill this with table name description extracted from COMMENT sub-clause of table_ddl
                                }
                            ],
                            "topics": [] # Fill this with topic info
                        }
                    }

                    output.append(table_info)

    finally:
        connection.close()

    return output


def get_non_system_tables(host, username, password, database):
    # Connect to MySQL
    connection = pymysql.connect(
        host=host,
        user=username,
        password=password,
        database=database
    )

    cursor = connection.cursor(pymysql.cursors.DictCursor)

    # Query to get table names of non-system tables
    query = """
    SELECT table_schema, table_name
    FROM information_schema.tables
    WHERE table_schema NOT IN ('information_schema', 'mysql', 'performance_schema', 'sys')
    AND table_type = 'BASE TABLE'
    """

    cursor.execute(query)

    tables = []
    for row in cursor.fetchall():
        tables.append({
            'schema_name': row['table_schema'],
            'table_name': row['table_name']
        })

    cursor.close()
    connection.close()

    return tables


if __name__=="__main__":
    # Usage example
    json_output = extract_table_info("118.195.233.54","root","aituno2024","employees")
    print(json.dumps(json_output, indent=4))
