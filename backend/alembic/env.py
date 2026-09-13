import os
import re
from logging.config import fileConfig

# Load environment variables from .env file
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlmodel import SQLModel

from alembic import context

# import models
from src.auth.models import *
from src.category.models import *
from src.comment.models import *
from src.post.models import *
from src.tag.models import *

load_dotenv()  # This loads .env from current directory

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
target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

url_tokens = {
    "DB_USER": os.getenv("POSTGRES_USER", ""),
    "DB_PASS": os.getenv("POSTGRES_PASSWORD", ""),
    "DB_HOST": os.getenv("POSTGRES_HOST", ""),
    "DB_PORT": os.getenv("POSTGRES_PORT", 5432),
    "DB_NAME": os.getenv("POSTGRES_DB", ""),
}

url = config.get_main_option("sqlalchemy.url") or ""

url = re.sub(r"\${(.+?)}", lambda m: url_tokens[m.group(1)], url)


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
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    from alembic.operations import ops

    def _filter_drop_indexes(directives, tables_dropped):
        # given a set of (tablename, schemaname) to be dropped, filter
        # out DropIndexOp from the list of directives and yield the result.

        for directive in directives:
            # ModifyTableOps is a container of ALTER TABLE types of
            # commands.  process those in place recursively.
            if (
                isinstance(directive, ops.ModifyTableOps)
                and (directive.table_name, directive.schema) in tables_dropped
            ):
                directive.ops = list(
                    _filter_drop_indexes(directive.ops, tables_dropped)
                )

                # if we emptied out the directives, then skip the
                # container altogether.
                if not directive.ops:
                    continue
            elif (
                isinstance(directive, ops.DropIndexOp)
                and (directive.table_name, directive.schema) in tables_dropped
            ):
                # we found a target DropIndexOp.   keep looping
                continue

            # otherwise if not filtered, yield out the directive
            yield directive

    def process_revision_directives(context, revision, directives):
        script = directives[0]

        # process both "def upgrade()", "def downgrade()"
        for directive in (script.upgrade_ops, script.downgrade_ops):
            # make a set of tables that are being dropped within
            # the migration function
            tables_dropped = set()
            for op in directive.ops:
                if isinstance(op, ops.DropTableOp):
                    tables_dropped.add((op.table_name, op.schema))

            # now rewrite the list of "ops" such that DropIndexOp
            # is removed for those tables.   Needs a recursive function.
            directive.ops = list(_filter_drop_indexes(directive.ops, tables_dropped))

    # connectable = engine_from_config(
    #     config.get_section(config.config_ini_section, {}),
    #     prefix="sqlalchemy.",
    #     poolclass=pool.NullPool,
    # )

    connectable = create_engine(url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
