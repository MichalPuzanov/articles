# Using Alembic for SQLModel Database Migrations

Upgrading a database schema in the `SQLAlchemy` ORM can be difficult. Alembic, created by the author of `SQLAlchemy`, is a lightweight database migration tool that addresses this problem.

Because `SQLModel` is built directly on top of `SQLAlchemy`, it integrates well with Alembic. In simple terms, Alembic provides version control for a database schema, in much the same way that `Git` provides version control for source code.

## The Limitation of `SQLModel.metadata.create_all()`

When an application starts, it can call `SQLModel.metadata.create_all(engine)`. This command creates tables that do not already exist. However, it does not modify tables that have already been created. It checks whether the tables exist, but does not compare their complete definitions.

For example, if a model gains a new column, `create_all()` does not add that column to an existing table. The application may then encounter errors when it attempts to use the updated model with the old database schema.

## What Alembic Provides

When an application's code changes, for example when a column is added or a table is removed, the database schema does not update automatically.

Without a migration tool, we would need to write and execute raw SQL commands manually on every computer or server running the application. This approach could result in data loss, an incomplete migration history, and significant maintenance difficulties.

## Key Features of Alembic

- **Incremental versioning:** Each change to the database schema is recorded in a time-stamped revision script, such as `1a2b3c4d_add_age_column.py`, in the project's `versions/` folder.
- **Autogeneration:** Alembic compares the SQLModel metadata with the current database schema and generates a proposed migration script.
- **Upgrades and downgrades:** Each migration file contains an `upgrade()` function for applying changes and a `downgrade()` function for reversing them when appropriate.
- **Database support:** Alembic generates SQL appropriate for supported database systems, including PostgreSQL, MySQL, SQLite, Oracle, and SQL Server.

## How Alembic Works

When we run `alembic revision --autogenerate -m \"<message>\"`, Alembic performs three main steps:

1. **Inspect the database:** It reads the database to identify the tables, columns, indexes, and constraints that currently exist.
2. **Inspect the models:** It reads the Python models registered in the SQLModel metadata.
3. **Calculate the differences:** It compares the model metadata with the database schema and writes the proposed operations to a new revision file.

### What It Detects

Autogeneration can identify many common schema changes, including:

- Newly added or removed tables.
- Newly added or removed columns.
- Changes to whether a column permits null values (`nullable=True` or `nullable=False`).
- Newly added or removed indexes and unique constraints.
- Newly added or removed foreign-key relationships.

### Issues and Limitations

The `--autogenerate` option is useful, but it has limitations and its output must always be reviewed.

- **Column type changes require verification:** Alembic can compare column types when type comparison is enabled, but the result may depend on the Alembic version, database dialect, and configuration. Check the generated migration and configure `compare_type=True` in the `context.configure()` call in `env.py` when required.
- **Schema-object renaming is ambiguous:** If, for example, a column is renamed, Alembic may interpret the change as dropping the old column and creating a new one. This can result in data loss. Modify the generated revision manually so that the existing data is preserved before running `alembic upgrade head`.
- **Models must be available:** If Alembic cannot access the models when a revision is generated, it may interpret the entire schema as deleted and generate destructive operations. Always inspect the generated revision before applying it to the database.

## Practical Examples

### Installation

The examples require the external libraries `sqlmodel` and `alembic`. They also use two Python standard-library modules: `typing` for type annotations and `sqlite3` for the SQLite database used during testing.

*Using pip:*

```bash
pip install sqlmodel alembic
```

### Initialise Alembic

From the project root, initialise the Alembic migration environment:

```bash
alembic init _db_migration
```

This command creates the `_db_migration` folder and an `alembic.ini` configuration file.

### Configure the Database URL

Open `alembic.ini` and locate the `sqlalchemy.url` property. Change it so that it points to the target database. The following example specifies a PostgreSQL database:

```
sqlalchemy.url = postgresql://user:password@localhost:5432/dbname
```

For the examples in this notebook, we use an `SQLite` database named `test.db`, created in the application's root directory:

```
sqlalchemy.url = sqlite:///test.db
```

### Link SQLModel to Alembic (`_db_migration/env.py`)

Alembic must have access to the model metadata in order to autogenerate migrations. Create a `models` folder in the application's root directory, then edit `_db_migration/env.py` as follows:

```python
# 1. Import SQLModel
from sqlmodel import SQLModel

# 2. Import the models so that SQLModel registers them
import models

# 3. Set target_metadata to the SQLModel metadata
target_metadata = SQLModel.metadata
```

### Prevent Missing Type Errors (`_db_migration/script.py.mako`)

`SQLModel` uses specific type wrappers. Consequently, generated migration scripts may raise an error unless `sqlmodel` is imported into them. Open `_db_migration/script.py.mako`, the template used to create new migration scripts, and add `import sqlmodel` to the imports section:

```python
\"\"\"${message}\"\"\"
revision = '${up_revision}'
down_revision = '${down_revision}'
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}

from alembic import op
import sqlalchemy as sa
import sqlmodel
${imports}
```

### Workflow for Creating or Updating the Database

Whenever we create a new model or modify an existing schema, we should follow these three steps:

- **Step A: Define or modify the SQLModel**

  Create a new model in the `models` folder. For example, we can create `user_model.py`:

  ```python
  from typing import Optional
  from sqlmodel import Field, SQLModel

  class User(SQLModel, table=True):
      id: Optional[int] = Field(default=None, primary_key=True)
      username: str = Field(index=True)
      email: str
      age: Optional[int] = None  # Added column
  ```

  Update `__init__.py` to import the new `User` model:

  ```python
  from .user_model import User
  ```

- **Step B: Autogenerate the migration script**

  Run the `revision` command with the `--autogenerate` option. Alembic compares the model metadata with the live database schema and writes a proposed migration script to the `_db_migration/versions` folder:

  ```bash
  alembic revision --autogenerate -m \"created user table\"
  ```

- **Step C: Apply the changes to the database**

  Review the generated migration, then use the `upgrade` command to apply it and move the database to the latest revision, known as `head`:

  ```bash
  alembic upgrade head
  ```

### Other Useful Alembic Commands

- **Roll back changes**

  Use the `downgrade` command to reverse changes. The following command rolls the database back by one revision:

  ```bash
  alembic downgrade -1
  ```

- **View the revision history**

  Use the `history` command to view the revision history:

  ```bash
  alembic history
  ```

- **View the current database revision**

  Use the `current` command to display the latest revision applied to the database:

  ```bash
  alembic current
  ```

- **View the current code revision (`head`)**

  Use the `heads` command to display the latest revision in the migration files:

  ```bash
  alembic heads
  ```

- **Remove a head revision**

  There are three possible situations:

  1. **The head revision has not yet been applied to the database**

     If a migration file was created with `--autogenerate` but `alembic upgrade head` has not been run, the database does not yet reference that revision. Open `_db_migration/versions/`, locate the `.py` file matching the head revision ID, and delete it. The migration history will then return to the previous revision.

  2. **The head revision has already been applied to the database**

     First, downgrade the database. This tells Alembic to reverse the changes made by the head revision and move the database tracker back by one revision:

     ```bash
     alembic downgrade -1
     ```

     Next, delete the head revision `.py` file from the `_db_migration/versions/` folder.

  3. **The revision file has been deleted, but the database still refers to it**

     The migration can become stuck if the revision file is deleted before the database is downgraded. Alembic then looks for a revision ID whose file no longer exists.

     To resolve this situation, stamp the database with the current head revision:

     ```bash
     alembic stamp head
     ```

     The `stamp` command does not change the database schema. It updates Alembic's internal revision tracking so that new migrations can be generated again. Use this command only when the database schema already matches the stamped revision.

## Conclusion

Alembic provides the version-control layer between a changing SQLModel application and its database. Instead of relying on `SQLModel.metadata.create_all(engine)`, which does not update existing tables, we can record each schema change as a migration and apply it in a controlled and repeatable manner.

The core workflow is straightforward: define or modify a SQLModel, generate a revision with `alembic revision --autogenerate`, review the generated operations, and apply them with `alembic upgrade head`. Commands such as `downgrade`, `history`, `current`, and `heads` help us inspect and manage the migration history as the project evolves.

Autogeneration is an excellent starting point, but it is not a substitute for review. Ensure that all models are imported, enable type comparison when necessary, and handle renames manually so that existing data is preserved. With these practices, Alembic and SQLModel make database changes easier to track, test, roll back, and deploy safely across development and production environments.

