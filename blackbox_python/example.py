from blackbox import BlackBox

EXAMPLE_SQL_QUERY = "SELECT * FROM source_histories LIMIT 10;"

with BlackBox() as bb:
    data = bb.query(EXAMPLE_SQL_QUERY)
    print(data.head(3))
