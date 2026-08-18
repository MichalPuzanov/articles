# Introduction to the Python SQLModel Library

`SQLModel` is a modern Python ORM (Object-Relational Mapping) library that enables us to use ordinary Python classes and objects to interact with databases. It substantially reduces the need to write raw SQL queries. Created by the author of `FastAPI`, `SQLModel` combines `SQLAlchemy`, a powerful Python ORM, with `Pydantic`, a robust data-validation library, in a single tool. This is the first article in a mini-series about `SQLModel`; it introduces the library through a set of basic examples.

## The Core Problems It Solves

When building a Python web API that uses a database, we traditionally need to define two separate models for almost identical data:

- **SQLAlchemy model:** Defines the database tables and columns.
- **Pydantic model:** Validates and parses incoming HTTP data.

This approach creates substantial code duplication and increases maintenance overhead. SQLModel addresses both problems by combining data validation and database-table definitions in a single model. It also enables Python developers to work with SQL databases without requiring extensive knowledge of SQL.

## Key Features

- **No code duplication:** Define fields once. The class functions simultaneously as an API-schema layer and a database mapping.
- **Excellent IDE support:** `SQLModel` relies heavily on native Python type hints, enabling code editors to provide detailed autocompletion and highlight type errors directly in the IDE.
- **Built on established libraries:** SQLModel does not reinvent the wheel. It uses `SQLAlchemy` and `Pydantic` internally, allowing developers to benefit from the full capabilities of both libraries.
- **FastAPI integration:** SQLModel was designed to fit naturally into the FastAPI ecosystem, although it also works well with other Python applications.

## Practical Examples

### Installation

Only one external library `sqlmodel` is required. The examples also use two Python standard-library modules: `typing` for type annotations and `sqlite3` for the SQLite database used during testing.

*Using pip:*

```bash
pip install sqlmodel
```

### Installation Verification


```python
import sqlmodel

print("SQLModel version:", sqlmodel.__version__)
```

    SQLModel version: 0.0.39


### Basic Code Example

In this example, we declare a database table and perform several operations using `SQLModel`.


```python
from typing import Optional
from sqlmodel import  create_engine, Field, Session, select, SQLModel

# Run this line to clear memory BEFORE defining your classes, we 
SQLModel.metadata.clear()

# Define a simple model using both SQLAlchemy and Pydantic features
class User(SQLModel, table=True, tablename="users"):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    prefered_name: str
    age: Optional[int] = None
    
# Create an SQLite database engine
engine = create_engine("sqlite:///test_db.db")

# Create the database tables
SQLModel.metadata.create_all(engine)

# Create a new user instance
new_user = User(name="John Doe", prefered_name="Johnny", age=30)

# Add the new user to the database
with Session(engine) as session:
    session.add(new_user)
    session.commit()
    
# Query the database to retrieve the user
with Session(engine) as session:
    statement = select(User).where(User.name == "John Doe")
    result = session.exec(statement)
    user = result.first()
    print(user)

```

    name='John Doe' id=1 prefered_name='Johnny' age=30


The preceding code creates a SQLite database. Because the code is executed in a Jupyter Notebook, `SQLModel.metadata.clear()` is used to prevent conflicts with schemas from previous executions. This step is not normally required when using a standard Python client. We then call `SQLModel.metadata.create_all()` to create the tables and add new records to them.

Let us now examine the most commonly used arguments of `create_engine()`.

### Connection Configuration

- **`url` (string or URL object):** The first positional argument specifies the database dialect, driver, connection credentials, and database name.

```python
# Format: dialect+driver://username:password@host:port/database
create_engine("postgresql+psycopg2://scott:tiger@localhost:5432/mydatabase")
```

- **`connect_args`:** Passes driver-specific options directly to the underlying database driver.

```python
# Essential for SQLite multi-threading in web applications
create_engine("sqlite:///db.sqlite", connect_args={"check_same_thread": False})
```

- **`echo`:** When set to `True`, the engine logs each SQL statement that it generates to the terminal. This is useful for debugging but should generally be disabled in production.

```python
create_engine("sqlite:///db.sqlite", echo=True)
```

### Connection Pool Tuning for Production

Relational databases can become less efficient if they repeatedly open and close connections. The engine therefore maintains a pool of active connections that can be reused.

- **`pool_size`:** The number of persistent database connections to keep open in the pool.
- **`max_overflow`:** The number of additional connections that may be opened temporarily when the pool reaches its `pool_size` during periods of high traffic.
- **`pool_timeout`:** The number of seconds the application waits for a connection from the pool before raising a timeout error.

### Using an In-Memory SQLite Database: The `poolclass` Parameter

The `poolclass` parameter tells `SQLAlchemy`, which is used by `SQLModel`, how to manage and cache database connections. In most cases, the default pool is sufficient. However, an in-memory SQLite database requires particular care: the database is deleted when its connection count falls to zero. Using the `StaticPool` class keeps a single connection available, preventing the data from disappearing between requests.


```python
from typing import Optional
from sqlmodel import  create_engine, Field, Session, select, SQLModel
from sqlmodel.pool import StaticPool

# Run this line to clear memory BEFORE defining your classes
SQLModel.metadata.clear()

# Define a simple model using both SQLAlchemy and Pydantic features
class User(SQLModel, table=True, tablename="users"):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    prefered_name: str
    home_address: Optional[str] = None
    age: Optional[int] = None
    
# Create an SQLite database engine
engine = create_engine("sqlite:///:memory:", poolclass=StaticPool)

# Create the database tables
SQLModel.metadata.create_all(engine)

# Create a new user instance
new_user = User(name="John Doe", prefered_name="Johnny", home_address="123 Main St", age=30)
new_user1 = User(name="Anthony House", prefered_name="Tony", home_address="432 Hotel St", age=45)
new_user2 = User(name="Anthony Housic", prefered_name="Tonda", home_address="432 Hotel St", age=34)
# Add the new user to the database
with Session(engine) as session:
    new_user = User(name="John Doe", prefered_name="Johnny", home_address="123 Main St", age=30)
    session.add(new_user)
    session.commit()
    

with Session(engine) as session:
    new_user1 = User(name="Anthony House", prefered_name="Tony", home_address="432 Hotel St", age=45)
    new_user2 = User(name="Anthony Housic", prefered_name="Tonda", home_address="432 Hotel St", age=34)
    session.add(new_user1)
    session.add(new_user2)
    session.commit()
    
# Query the database to retrieve the user
with Session(engine) as session:
    statement = select(User)
    result = session.exec(statement)
    for user in result:
        print(user)
    
    print("Your current pool class is:", engine.pool.__class__.__name__)

```

    name='John Doe' id=1 home_address='123 Main St' age=30 prefered_name='Johnny'
    name='Anthony House' id=2 home_address='432 Hotel St' age=45 prefered_name='Tony'
    name='Anthony Housic' id=3 home_address='432 Hotel St' age=34 prefered_name='Tonda'
    Your current pool class is: StaticPool


    /home/michal-puzanov/.pyenv/versions/articles/lib/python3.12/site-packages/sqlmodel/main.py:681: SAWarning: This declarative base already contains a class with the same class name and module name as __main__.User, and will be replaced in the string-lookup table.
      DeclarativeMeta.__init__(cls, classname, bases, dict_, **kw)


The example works as expected. However, in recent versions of `SQLModel` and `SQLAlchemy` explicitly specifying the pool class is often unnecessary because the engine selects an appropriate pool based on the database type. The following example demonstrates this behaviour.


```python
# in-memory sqlite database
engine = create_engine("sqlite:///:memory:")
print("Your in-memory pool class is:", engine.pool.__class__.__name__)

# file sqlite database
engine = create_engine("sqlite:///test_db.db")
print("Your file pool class is:", engine.pool.__class__.__name__)
```

    Your in-memory pool class is: SingletonThreadPool
    Your file pool class is: QueuePool


The output shows that the default pool differs according to the database engine. An in-memory SQLite database can operate without additional configuration in a single-threaded notebook, whereas web applications and multi-threaded environments may require explicit settings such as `StaticPool` and `check_same_thread=False`. Selecting the pool deliberately helps ensure that database connections remain available for the required lifetime and prevents unexpected data loss.

## Conclusion

SQLModel provides a clear way to work with relational databases using familiar Python types and classes. In this article, we defined a model, created a SQLite database, inserted records, queried them with `select()`, and examined how engine configuration affects database connections. The examples also demonstrated that a single model can combine Pydantic validation with SQLAlchemy database behaviour, reducing duplication while retaining access to established SQLAlchemy features.

For small applications and prototypes, SQLModel offers a productive starting point with very little boilerplate. In production systems, however, it remains important to understand the underlying database, configure the engine for the deployment environment, and manage sessions carefully. With these principles in place, SQLModel can provide a practical foundation for building typed Python applications that use relational data.

Did this article help you? Let me know in the comments below, and don't forget to drop a like if you enjoyed the read! Thank you.
