from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from urllib.parse import quote
from alembic import context
from app.models import Base
# import os
from app.config import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# mysql_user = os.environ.get("MYSQL_USER")
# mysql_pass = os.environ.get("MYSQL_PASS")
# pgsql_user = os.environ.get("PGSQL_USER")
# pgsql_pass = os.environ.get("PGSQL_PASS")

# mysql_url = f"mysql://{mysql_user}:%s@localhost:3306/fastapi" % quote(mysql_pass)
pgsql_url = f"postgresql+psycopg2://{settings.database_username}:%s@{settings.database_hostname}" \
            f":{settings.database_port}/{settings.database_name}" % quote(settings.database_password)

# In Alembic "%" creates an issue and hence has to be escaped:
# https://stackoverflow.com/questions/39849641/in-flask-migrate-valueerror-
# invalid-interpolation-syntax-in-connection-string-a
db_url_escaped = pgsql_url.replace('%', '%%')


config.set_main_option("sqlalchemy.url", db_url_escaped)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
