"""PostgresTransaction — run multiple statements in a transaction."""


class PostgresTransaction:
    """Execute multiple SQL statements within a single transaction.

    Reads: ``statements`` (list of {sql, params?} dicts), ``dsn`` (or passed at init).
    Writes: ``transaction_results`` (list of affected row counts).
    """

    def __init__(self, dsn: str = ""):
        self._dsn = dsn

    def call(self, payload):
        import psycopg2

        dsn = self._dsn or payload.get("dsn")
        stmts = payload.get("statements") or []
        conn = psycopg2.connect(dsn)
        results = []
        try:
            with conn.cursor() as cur:
                for stmt in stmts:
                    cur.execute(stmt["sql"], stmt.get("params") or None)
                    results.append(cur.rowcount)
            conn.commit()
            return payload.insert("transaction_results", results)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
