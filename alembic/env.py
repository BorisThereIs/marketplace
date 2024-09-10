from logging.config import fileConfig
from typing import Union

from sqlalchemy import MetaData, Table, engine_from_config, pool

from alembic import context

from config.settings import CONN_STRING

from models import metadata_to_migrate


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata: MetaData = metadata_to_migrate

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

x_kwargs = context.get_x_argument(as_dictionary=True)

def include_object(object, name, type_, reflected, compare_to):
    if table_name := x_kwargs.get('table', None):
        if type_ == 'table' and name != table_name:
            return False
    return True


def narrow_target_metadata(table_name: str) -> None:
    table_instance: Union[Table, None] = None
    if table_name in target_metadata.tables.keys():
        table_instance = target_metadata.tables[table_name]
        target_metadata.clear()
        target_metadata._add_table(name=table_instance.name, schema=None, table=table_instance)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # url = config.get_main_option("sqlalchemy.url")
    url = CONN_STRING
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=CONN_STRING,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


if x_kwargs.get('table'):
    narrow_target_metadata(x_kwargs['table'])

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
