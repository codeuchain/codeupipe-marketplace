"""PostgresQuery — execute SELECT queries."""


class PostgresQuery:
    """Execute a SELECT query and return rows.

    Reads: ``sql``, ``params`` (optional), ``dsn`` (or passed at init).
    Writes: ``rows`` (list of dicts), ``row_count``.
    """

    def __init__(self, dsn: str = ""):
        self._dsn = dsn

    def call(self, payload):
        import psycopg2
        import psycopg2.extras

        dsn = self._dsn or payload.get("dsn")
        conn = psycopg2.connect(dsn)
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(payload.get("sql"), payload.get("params") or None)
                rows = [dict(r) for r in cur.fetchall()]
            return payload.insert("rows", rows).insert("row_count", len(rows))
        finally:
            conn.close()
