from base import Session, engine, Base
from modals import *
# 2 - generate database schema
Base.metadata.create_all(engine)

# 3 - create a new session
session = Session()
session.add(Hi(25))
session.commit()
session.close()