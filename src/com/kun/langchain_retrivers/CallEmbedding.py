import psycopg2
from psycopg2 import sql

def call_postgres_function(conn, function_name, *args):
    # Create a cursor
    cursor = conn.cursor()

    try:
        # Construct the function call query
        query = sql.SQL("SELECT {}({})").format(
            sql.Identifier(function_name),
            sql.SQL(', ').join(map(sql.Literal, args))
        )

        # Execute the function call query
        cursor.execute(query)

        # If the function returns a result, fetch it
        result = cursor.fetchall()

        # Commit the transaction
        conn.commit()

        return result

    except Exception as e:
        # Rollback the transaction if an error occurs
        conn.rollback()
        print("Error calling PostgreSQL function:", e)

    finally:
        # Close cursor
        cursor.close()


# Example usage
if __name__=="__main__":
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname='aituno',
            user='postgres',
            password='111111',
            host='localhost',
            port='5466'
        )

        # Call the PostgreSQL function
        result = call_postgres_function(conn, 'kw_match_documents', "spark", 10)
        for record in result:
            print("Function result:", record)

    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL:", e)

    finally:
        # Close the connection
        if conn:
            conn.close()