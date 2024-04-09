import os
from dotenv import load_dotenv
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

load_dotenv()
# Creates the Base and Session for Database
# DATABASE_URL_AUX = os.getenv("DATABASE_URL", "")
DATABASE_URL_AUX = os.getenv("DATABASE_URL", "")

if DATABASE_URL_AUX and DATABASE_URL_AUX.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL_AUX.replace("postgres://", "postgresql://", 1)
else:
    DATABASE_URL = DATABASE_URL_AUX

print("DATABASE URL in database.py: " + DATABASE_URL)

metadata = MetaData()
Base: DeclarativeMeta = declarative_base(metadata=metadata)


class Session:
    __engine = create_engine(DATABASE_URL, connect_args={"connect_timeout": 5})
    __SessionImpl = sessionmaker(bind=__engine)

    def __init__(self):
        self.__session_impl = self.__SessionImpl()

    def __getattr__(self, attr):
        """A Proxy to the real session implmentation"""

        return getattr(self.__session_impl, attr)

    def __del__(self):
        """
        Called by CPython's garbage collector after the reference count for this instance drops to zero.

        Automatically closes the session inner pointer (the real implementation),
        as soon there is no pointer to this Session instance (self)

        BEFORE (using a function generator called "get_session"):

        def some_function(session: sqlalchemy.orm.Session = Depends(dependencies.get_session)):
            ... # some code logic



        NOW (with a Proxy | Pointer to Implementation):

        def some_function(session: database.Session = Depends()):
            ... # some code logic
        """

        self.__session_impl.close()
