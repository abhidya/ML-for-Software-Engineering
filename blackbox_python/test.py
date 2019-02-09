from blackbox import BlackBox

with BlackBox() as bb:
    data = bb.query("SELECT COUNT(*) FROM source_histories;")
