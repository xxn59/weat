from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
food = Table('food', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=10)),
    Column('price', Integer, default=ColumnDefault(0)),
    Column('cat', Enum),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String(length=64)),
    Column('floor', Integer, default=ColumnDefault(23)),
    Column('cell', Integer),
    Column('email', String(length=120)),
    Column('level', Integer),
    Column('group', String(length=20)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['food'].columns['cat'].create()
    post_meta.tables['user'].columns['group'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['food'].columns['cat'].drop()
    post_meta.tables['user'].columns['group'].drop()
