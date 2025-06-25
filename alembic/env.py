import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from hiremebackend.database_module import Base
from hiremebackend import models  # ensure Alembic sees models

from dotenv import load_dotenv
load_dotenv()

config = context.config

# Load from environment
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise Exception("DATABASE_URL environment variable not set")

config.set_main_option("sqlalchemy.url", database_url)

# Logging
fileConfig(config.config_file_name)

# ✅ Use your models' metadata
target_metadata = Base.metadata

def run_migrations_offline():
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
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
