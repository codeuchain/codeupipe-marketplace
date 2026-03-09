# codeupipe-postgres

PostgreSQL queries, transactions, and bulk insert for codeupipe pipelines.

## Install

```bash
cup marketplace install codeupipe-postgres
```

## Filters

| Filter | Description |
|--------|-------------|
| `PostgresQuery` | Execute SELECT queries |
| `PostgresExecute` | Execute INSERT/UPDATE/DELETE |
| `PostgresTransaction` | Run multiple statements in a transaction |
| `PostgresBulkInsert` | Bulk insert rows efficiently |

## Usage

```python
from codeupipe import Payload, Pipeline
from codeupipe_postgres import PostgresQuery

pipeline = Pipeline()
pipeline.add_filter(PostgresQuery(dsn="postgresql://..."), name="query")

result = await pipeline.run(Payload({"sql": "SELECT * FROM users LIMIT 10"}))
print(result.get("rows"))
```
