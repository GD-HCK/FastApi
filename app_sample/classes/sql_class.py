import pyodbc
from ..configuration import get_connection_string

conn_str = get_connection_string()

def run_query_get(query: str, *params) -> list:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(query, *params)
    results = cursor.fetchall()
    result_list = []
    for result in results:
        dictionary = dict(zip([column[0] for column in cursor.description], result))
        values = result
        result_list.append({'dictionary': dictionary, 'values': values})
    conn.close()
    return result_list

def run_query_post(query: str, *params) -> int:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(query, *params)
    conn.commit()
    conn.close()
    return 1