from django.db import connections


def __dbconnection(db):
    return connections[db].cursor()


def query_executor(sql_query, db='default'):
    with __dbconnection(db) as cursor:
        cursor.execute(sql_query)
        return cursor.fetchone()