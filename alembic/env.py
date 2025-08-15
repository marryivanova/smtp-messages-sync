from logging.config import fileConfig
from alembic import context
from sqlalchemy import create_engine

from src.db.models import Base
from src.config.settings import settings

target_metadata = Base.metadata

config = context.config


DB_HOST = str(settings.DB_HOST)
DB_PORT = str(settings.DB_PORT)
DB_NAME = str(settings.DB_NAME)
DB_USER = str(settings.DB_USER)
DB_PASSWORD = str(settings.DB_PASSWORD)

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

config.set_main_option("sqlalchemy.url", DB_URL)

section = config.config_ini_section
config.set_section_option(section, "DB_HOST", DB_HOST)
config.set_section_option(section, "DB_PORT", DB_PORT)
config.set_section_option(section, "DB_NAME", DB_NAME)
config.set_section_option(section, "DB_USER", DB_USER)
config.set_section_option(section, "DB_PASSWORD", DB_PASSWORD)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=None,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(DB_URL)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()