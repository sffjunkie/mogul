from sqlalchemy import MetaData, ForeignKey
from sqlalchemy import Table, Column, String, Integer, Date

metadata = MetaData()

album = Table('album', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
)

# band (music), cast (movie)
group = Table('group', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
)

group_membership = Table('group_membership', metadata,
    Column('group', Integer, ForeignKey('group.id')),
    Column('person', Integer, ForeignKey('person.id')), # person or group?
    Column('role', Integer, ForeignKey('role.id')),
    Column('joined', Date),
    Column('left', Date),
    Column('thumbnail', String),
)

movie = Table('movie', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('year', Integer),
    Column('director', Integer, ForeignKey('person.id')),
    Column('cast', Integer, ForeignKey('group.id')),
    Column('thumbnail', String),
)

person = Table('person', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('born', Date),
    Column('died', Date),
    Column('thumbnail', String),
)

person_alias = Table('person_alias', metadata,
    Column('person', Integer, ForeignKey('person.id'), primary_key=True),
    Column('alias', String, primary_key=True),
)

# Director, Composer, Singer, Drummer, Bassist, Writer, Producer
role = Table('role', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
)

