import blackbox

EXAMPLE_SQL_QUERY = "SELECT * FROM source_histories LIMIT 10;"

with blackbox.BlackBox() as bb:
    data = bb.query(EXAMPLE_SQL_QUERY)
    for index, row in data.iterrows():
        print(row.content)
        print("NEXT CODE")
