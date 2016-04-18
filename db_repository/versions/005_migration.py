from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
cuisine = Table('cuisine', post_meta,
    Column('salad_id', Integer),
    Column('food_id', Integer),
)

food = Table('food', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=10)),
    Column('price', Integer, default=ColumnDefault(0)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['cuisine'].create()
    post_meta.tables['food'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['cuisine'].drop()
    post_meta.tables['food'].drop()
