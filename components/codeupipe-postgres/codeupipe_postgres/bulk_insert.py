"""PostgresBulkInsert — efficient bulk row insertion."""


class PostgresBulkInsert:
    """Bulk insert rows into a table.

    Reads: ``table``, ``rows`` (list of dicts), ``dsn`` (or passed at init).
    Writes: ``inserted_count``.
    """

    def __init__(self, dsn: str = ""):
        self._dsn = dsn

    def call(self, payload):
        import psycopg2
        import psycopg2.extras

        dsn = self._dsn or payload.get("dsn")
        table = payload.get("table")
        rows = payload.get("rows") or []
        if not rows:
            return payload.insert("inserted_count", 0)

        columns = list(rows[0].keys())
        conn = psycopg2.connect(dsn)
        try:
            with conn.cursor() as cur:
                values_list = [[row[c] for c in columns] for row in rows]
                template = "(" + ",".join(["%s"] * len(columns)) + ")"
                cols = ",".join(columns)
                query = f"INSERT INTO {table} ({cols}) VALUES %s"
                psycopg2.extras.execute_values(cur, query, values_list, template)
            conn.commit()
            return payload.insert("inserted_count", len(rows))
        finally:
            conn.close()
