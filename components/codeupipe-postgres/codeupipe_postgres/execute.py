"""PostgresExecute — execute INSERT/UPDATE/DELETE statements."""


class PostgresExecute:
    """Execute a write statement (INSERT, UPDATE, DELETE).

    Reads: ``sql``, ``params`` (optional), ``dsn`` (or passed at init).
    Writes: ``affected_rows``.
    """

    def __init__(self, dsn: str = ""):
        self._dsn = dsn

    def call(self, payload):
        import psycopg2

        dsn = self._dsn or payload.get("dsn")
        conn = psycopg2.connect(dsn)
        try:
            with conn.cursor() as cur:
                cur.execute(payload.get("sql"), payload.get("params") or None)
                affected = cur.rowcount
            conn.commit()
            return payload.insert("affected_rows", affected)
        finally:
            conn.close()
