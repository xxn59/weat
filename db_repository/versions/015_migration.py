from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
salad_order_table = Table('salad_order_table', post_meta,
    Column('salad_id', Integer),
    Column('order_id', Integer),
)

order = Table('order', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('timestamp', DateTime),
    Column('status', Integer, default=ColumnDefault(1)),
    Column('price', Integer, default=ColumnDefault(0)),
    Column('cos_id', Integer),
    Column('meal', Enum),
    Column('remark', String(length=140)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['salad_order_table'].create()
    post_meta.tables['order'].columns['remark'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['salad_order_table'].drop()
    post_meta.tables['order'].columns['remark'].drop()
