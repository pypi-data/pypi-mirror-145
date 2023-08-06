# XQuery

### A package to easily run queries at SQL Server and BigQuery.

Allows sending queries and receiving data in form of pandas DataFrame from SQL Server and BigQuery.


# How to use
### SQL SERVER
```python
from xquery import XQuery

server_name = 'ENTER_SERV_NAME'
database_name = 'ENTER_DB_NAME'

sql_xq = XQuery()
sql_xq.set_connection_sql_server(server_name=server_name, database_name=database_name)
df = sql_xq.pull_query('SELECT 1 AS d')
print(df)
sql_xq.session.close_connection()
```



### BIGQUERY
```python
from xquery import XQuery
from src.XQuery.config import BQ_CLIENT_SECRET_FILE #  edit path to your file


bq_xq = XQuery()
bq_xq.set_connection_big_query(BQ_CLIENT_SECRET_FILE)
df = bq_xq.pull_query('SELECT 1 AS d')
print(df)
bq_xq.session.close_connection()
```
