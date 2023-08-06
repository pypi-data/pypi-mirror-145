import sqlalchemy.exc
from sqlalchemy import create_engine
from hermessplitter.db import tables

engine = create_engine('sqlite:///hdb.db')
engine.connect()
tables.metadata.create_all(engine)
try:
    ins = tables.settings.insert().values(
        key='active',
        value=True
    )
    engine.execute(ins)
except sqlalchemy.exc.IntegrityError:
    pass
