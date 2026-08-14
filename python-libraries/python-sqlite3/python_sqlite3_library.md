# Using SQL with Python's sqlite3 Library

The `sqlite3` module provides access to SQLite, a lightweight, serverless, and self-contained relational database management system. It is a wrapper around the SQLite C library that allows us to create, manage, and query databases directly using Structured Query Language (SQL), without setting up a separate database server such as MySQL or PostgreSQL. Its simplicity makes it particularly suitable for learning SQL, which is why it is used throughout this article.

## Key characteristics of the sqlite3 module

- **No configuration:** No installation or background server setup is required. The module is included in the standard Python distribution.
- **File-based storage:** The entire database, including its tables, indexes, and data, is stored in a single file on the local computer.
- **In-memory support:** Temporary databases can be created in computer memory. They are discarded when the script finishes, making them useful for testing.
- **Standards compliance:** The module follows the Python Database API Specification (PEP 249). This makes it easier to transfer knowledge to larger enterprise databases, although each SQL database system has its own specific differences.

## Core components

When using the module, we primarily interact with two fundamental objects:

- **Connection object:** Manages the connection to the database file, handles database transactions, and commits changes.
- **Cursor object:** Acts as a pointer or workhorse that executes SQL statements and retrieves the resulting rows.

The following sections present practical examples.

## Practical examples

### Verify the installation

The `sqlite3` module has been included in the standard Python distribution since version 2.5.


```python
import sqlite3

# Check SQLite version
print(f"SQLite version: {sqlite3.sqlite_version}")
```

    SQLite version: 3.45.1


### Create and connect to a database

We can create or connect to two types of database: a file-based database or an in-memory database. When connecting to a file-based database, SQLite checks whether the file already exists. If it does not, SQLite creates it automatically.

There are two general rules for connecting to a database:

1. **Local applications: one connection per application.** Open the connection at start-up, reuse it throughout the application, and close it during shutdown.
2. **Web applications: one connection per request.** Open the connection when a user makes a request, execute the necessary queries, and close it before sending the response.

*Create or connect to a file-based database*


```python
connection = sqlite3.connect('our_tests.db')
cursor = connection.cursor()

print("✓ Connected to SQLite database")
connection.close()
```

    ✓ Connected to SQLite database


*Connect to an in-memory database*


```python
# Connect to an in-memory SQLite database
connection = sqlite3.connect(':memory:')
cursor = connection.cursor()

print("✓ Connected to SQLite database")
connection.close()

```

    ✓ Connected to SQLite database


### Transactions

Transactions are important for two fundamental reasons:

1. **Data safety and integrity:** Transactions follow the ACID principles:
   - **Atomicity: all or nothing.** Every operation in a transaction must succeed, or the entire transaction is rolled back.
   - **Consistency: valid data only.** Updates must comply with all database constraints, rules, and data types.
   - **Isolation: independent execution.** Concurrent transactions cannot interfere with one another's work.
   - **Durability: permanent storage.** Once a transaction has been committed, the data is written to disk and survives system crashes or power failures.
2. **Improved performance:** When modifying a SQLite database, the computer must write the data to storage. Disk operations are considerably slower than operations in system memory.
   - **Without a transaction:** SQLite may need to open the file, write the change, and save it to disk for every individual operation. If we insert 10,000 rows, the computer may perform 10,000 relatively slow disk-write operations.
   - **With a transaction:** SQLite keeps the changes in memory until `commit()` is called, then writes all the rows to disk in a single operation.

### Create a table

We can create tables with various data types and constraints.

**Data types in SQLite**

- INTEGER: Whole numbers
- REAL: Floating-point numbers
- TEXT: Text strings
- BLOB: Binary data
- NULL: Missing values

**Common constraints**

- PRIMARY KEY: A unique identifier
- NOT NULL: The field must contain a value
- UNIQUE: Duplicate values are not permitted
- DEFAULT: A default value used when none is specified
- CHECK: A condition used to validate data


```python
import sqlite3

connection = sqlite3.connect(':memory:')

with connection:
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)')
    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Alice', 30))
    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Bob', 25))
    
with connection:
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

connection.close()
```

    (1, 'Alice', 30)
    (2, 'Bob', 25)


The first example creates an in-memory database and uses two transactions. The first transaction creates the `users` table, if it does not already exist, and inserts two records. The second transaction retrieves those records. Next, we will introduce an error into the first transaction by attempting to insert an invalid value for Alice's age.


```python
import sqlite3

connection = sqlite3.connect(':memory:')

with connection:
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)')
    # age is not INTEGER
    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Alice', 30.6))
    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Bob', 25))
    
with connection:
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

connection.close()
```

    (1, 'Alice', 30.6)
    (2, 'Bob', 25)


No error is raised in this example because SQLite uses dynamic typing. By default, the data type is associated with each individual value, or cell, rather than with the column. In many other database systems, the data type is associated with the column, which means that every value in that column must use the same data type. Fortunately, SQLite versions 3.37 and later support strict tables. We can enable this behaviour by adding `STRICT` to the end of the `CREATE TABLE` statement.


```python
import sqlite3

connection = sqlite3.connect(':memory:')

with connection:
    cursor = connection.cursor()
    # Adding STRICT forces strict data type enforcement
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER) STRICT')
    # age is not INTEGER
    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Alice', 30.6))
    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Bob', 25))
    
with connection:
    print("Another transaction that will not be executed due to the error above")

connection.close()
```


    ---------------------------------------------------------------------------

    IntegrityError                            Traceback (most recent call last)

    Cell In[41], line 10
          6     cursor = connection.cursor()
          7     # Adding STRICT forces strict data type enforcement
          8     cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER) STRICT')
          9     # age is not INTEGER
    ---> 10     cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Alice', 30.6))
         11     cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Bob', 25))
         12 
         13 with connection:


    IntegrityError: cannot store REAL value in INTEGER column users.age


The invalid value now raises an error, which is the intended behaviour. However, the error stops the first transaction and prevents the second transaction from running. The example is deliberately simple to demonstrate that an error can also prevent otherwise valid subsequent operations from being executed. We can use a `try`/`except` block to handle the error and allow the next transaction to proceed.


```python
import sqlite3

connection = sqlite3.connect(':memory:')

with connection:
    try:
        cursor = connection.cursor()
        # Adding STRICT forces strict data type enforcement
        cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER) STRICT')
        # age is not INTEGER
        cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Alice', 30.6))
        cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Bob', 25))
    except sqlite3.DatabaseError as e:
        print(f"Database error occurred: {e}")
    finally:
        #  Guarantees the cursor closes and frees memory
        cursor.close()
    
with connection:
    print("Another transaction that will be executed despite the previous error")

connection.close()
```

    Database error occurred: cannot store REAL value in INTEGER column users.age
    Another transaction that will be executed despite the previous error


We will now create the file-based database `our_tests.db`, which we will use throughout the remainder of the article, and add several tables to it.


```python
import sqlite3

conn = sqlite3.connect('our_tests.db')

with conn:
    try:
        cursor = conn.cursor()
        # Drop tables if they exist (for demo purposes)
        cursor.execute('DROP TABLE IF EXISTS users')

        # Create users table
        cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            age INTEGER CHECK(age >= 18),
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        ) STRICT''')
        
        # Create orders table if not exists with FOREIGN KEY
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            product TEXT NOT NULL,
            amount REAL,
            order_date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        ) STRICT''')
    except sqlite3.DatabaseError as e:
        print(f"Database error occurred: {e}")
    finally:
        cursor.close()

print("✓ Tables created successfully")

conn.close()
```

    ✓ Tables created successfully


### Insert data

We can insert either a single record or multiple records. Data insertion should be performed within a transaction.


```python
import sqlite3

conn = sqlite3.connect('our_tests.db')

with conn:
    try:
        cursor = conn.cursor()
        # Insert single row
        cursor.execute('''
            INSERT INTO users (name, email, age)
            VALUES (?, ?, ?)
        ''', ('Alice Johnson', 'alice@example.com', 28))

        # Insert multiple rows at once
        users_data = [
            ('Bob Smith', 'bob@example.com', 35),
            ('Carol White', 'carol@example.com', 42),
            ('David Brown', 'david@example.com', 31),
        ]
        cursor.executemany('''
            INSERT INTO users (name, email, age)
            VALUES (?, ?, ?)
        ''', users_data)
        
        # Insert orders data
        orders_data = [
            (1, 'Laptop', 999.99),
            (1, 'Mouse', 29.99),
            (2, 'Monitor', 299.99),
            (3, 'Keyboard', 79.99),
            (2, 'USB Cable', 9.99),
            (4, 'Headphones', 149.99),
        ]
        cursor.executemany('''
            INSERT INTO orders (user_id, product, amount)
            VALUES (?, ?, ?)
        ''', orders_data)

    except sqlite3.DatabaseError as e:
        print(f"Database error occurred: {e}")
    finally:
        cursor.close()

print("✓ Inserted users and orders successfully")

conn.close()
```

    ✓ Inserted users and orders successfully


### Use `SELECT` to query data

We can retrieve data from tables using various filtering and sorting options. `SELECT` statements are read-only: they do not modify the database, so there is normally no need to commit or roll back a transaction. Nevertheless, using a `try`/`except` block is good practice when executing database operations.

*Select all columns*


```python
import sqlite3

conn = sqlite3.connect('our_tests.db')
cursor = conn.cursor()

# SELECT all columns
query = 'SELECT * FROM users'
cursor.execute(query)
rows = cursor.fetchall()
print("All users:")
for row in rows:
    print(row)
```

    All users:
    (1, 'Alice Johnson', 'alice@example.com', 28, '2026-08-14 11:46:25')
    (2, 'Bob Smith', 'bob@example.com', 35, '2026-08-14 11:46:25')
    (3, 'Carol White', 'carol@example.com', 42, '2026-08-14 11:46:25')
    (4, 'David Brown', 'david@example.com', 31, '2026-08-14 11:46:25')


*Select specific columns*


```python
# SELECT specific columns
cursor.execute('SELECT name, email FROM users')
print("Names and emails:")
for name, email in cursor.fetchall():
    print(f"  {name}: {email}")
print()

# SELECT with WHERE clause
cursor.execute('SELECT name, age FROM users WHERE age > 30')
print("Users older than 30:")
for name, age in cursor.fetchall():
    print(f"  {name}: {age} years")
print()

# SELECT with ORDER BY
cursor.execute('SELECT name, age FROM users ORDER BY age DESC')
print("Users ordered by age (descending):")
for name, age in cursor.fetchall():
    print(f"  {name}: {age} years")
```

    Names and emails:
      Alice Johnson: alice@example.com
      Bob Smith: bob@example.com
      Carol White: carol@example.com
      David Brown: david@example.com
    
    Users older than 30:
      Bob Smith: 35 years
      Carol White: 42 years
      David Brown: 31 years
    
    Users ordered by age (descending):
      Carol White: 42 years
      Bob Smith: 35 years
      David Brown: 31 years
      Alice Johnson: 28 years


*Select a limited number of results*


```python
# SELECT with LIMIT
cursor.execute('SELECT name, age FROM users LIMIT 2')
print("First 2 users:")
for row in cursor.fetchall():
    print(f"  {row}")
print()

# SELECT with OFFSET (pagination)
cursor.execute('SELECT name, age FROM users LIMIT 2 OFFSET 2')
print("Users 3-4 (with OFFSET):")
for row in cursor.fetchall():
    print(f"  {row}")
print()

# fetchone() - get single row
cursor.execute('SELECT * FROM users WHERE id = 1')
user = cursor.fetchone()
print(f"User by ID (fetchone): {user}")

```

    First 2 users:
      ('Alice Johnson', 28)
      ('Bob Smith', 35)
    
    Users 3-4 (with OFFSET):
      ('Carol White', 42)
      ('David Brown', 31)
    
    User by ID (fetchone): (1, 'Alice Johnson', 'alice@example.com', 28, '2026-08-14 11:46:25')


### Use aggregate functions and `GROUP BY`

Aggregate functions such as `COUNT`, `SUM`, `AVG`, `MIN`, and `MAX` summarise data.

*Summarise data*


```python
# COUNT - count rows
cursor.execute('SELECT COUNT(*) FROM users')
count = cursor.fetchone()[0]
print(f"Total users: {count}")

# COUNT with WHERE
cursor.execute('SELECT COUNT(*) FROM users WHERE age > 30')
count = cursor.fetchone()[0]
print(f"Users over 30: {count}")
print()

# SUM - sum values
cursor.execute('SELECT SUM(amount) FROM orders')
total = cursor.fetchone()[0]
print(f"Total orders amount: ${total:.2f}")
print()

# AVG - average value
cursor.execute('SELECT AVG(amount) FROM orders')
avg_amount = cursor.fetchone()[0]
print(f"Average order amount: ${avg_amount:.2f}")
print()

# MIN and MAX
cursor.execute('SELECT MIN(amount), MAX(amount) FROM orders')
min_amount, max_amount = cursor.fetchone()
print(f"Order amount range: ${min_amount} - ${max_amount:.2f}")
print()
```

    Total users: 4
    Users over 30: 3
    
    Total orders amount: $3139.88
    
    Average order amount: $261.66
    
    Order amount range: $9.99 - $999.99
    


*Group data*


```python
# GROUP BY - aggregate by category
cursor.execute('''
    SELECT user_id, COUNT(*) as order_count, SUM(amount) as total_spent
    FROM orders
    GROUP BY user_id
    ORDER BY total_spent DESC
''')
print("Orders grouped by user:")
for user_id, count, total in cursor.fetchall():
    cursor.execute('SELECT name FROM users WHERE id = ?', (user_id,))
    name = cursor.fetchone()[0]
    print(f"  {name}: {count} orders, Total: ${total:.2f}")
print()

# HAVING clause - filter grouped results
cursor.execute('''
    SELECT user_id, COUNT(*) as order_count
    FROM orders
    GROUP BY user_id
    HAVING COUNT(*) > 1
''')
print("Users with more than 1 order:")
for user_id, count in cursor.fetchall():
    cursor.execute('SELECT name FROM users WHERE id = ?', (user_id,))
    name = cursor.fetchone()[0]
    print(f"  {name}: {count} orders")
```

    Orders grouped by user:
      Alice Johnson: 4 orders, Total: $2059.96
      Bob Smith: 4 orders, Total: $619.96
      David Brown: 2 orders, Total: $299.98
      Carol White: 2 orders, Total: $159.98
    
    Users with more than 1 order:
      Alice Johnson: 4 orders
      Bob Smith: 4 orders
      Carol White: 2 orders
      David Brown: 2 orders


### Use `JOIN`s to combine two tables

- **INNER JOIN:** Returns rows with matching values in both tables.
- **LEFT JOIN:** Returns all rows from the left table and matching rows from the right table.
- **RIGHT JOIN:** Returns all rows from the right table and matching rows from the left table. In SQLite, it can be simulated by reversing the tables in a `LEFT JOIN`.
- **FULL OUTER JOIN:** Returns all rows from both tables. In SQLite, it can be simulated by combining `LEFT JOIN` queries with `UNION`.

As noted above, **SQLite does not support `RIGHT JOIN` and `FULL OUTER JOIN` in all versions**, so these operations may need to be simulated. The following examples demonstrate these joins.

*Join examples*


```python
# INNER JOIN
print("INNER JOIN - Users and their orders:")
cursor.execute('''
    SELECT u.name, o.product, o.amount
    FROM users u
    INNER JOIN orders o ON u.id = o.user_id
    ORDER BY u.name
''')
for name, product, amount in cursor.fetchall():
    print(f"  {name}: {product} (${amount:.2f})")
print()

# LEFT JOIN - shows all users, even those without orders
print("LEFT JOIN - All users with their order count:")
cursor.execute('''
    SELECT u.name, COUNT(o.id) as order_count
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    GROUP BY u.name
''')
for name, count in cursor.fetchall():
    print(f"  {name}: {count} orders")
print()

# RIGHT JOIN - SQLite doesn't support RIGHT JOIN, but we can simulate it
# by swapping tables and using LEFT JOIN
print("RIGHT JOIN (simulated) - All orders with user info:")
cursor.execute('''
    SELECT u.name, o.product, o.amount
    FROM orders o
    LEFT JOIN users u ON o.user_id = u.id
    ORDER BY o.product
''')
for name, product, amount in cursor.fetchall():
    user = name if name else "Unknown"
    print(f"  {user}: {product} (${amount:.2f})")
print()

# FULL OUTER JOIN - SQLite doesn't support it, simulate with UNION
print("FULL OUTER JOIN (simulated with UNION) - All users and orders:")
cursor.execute('''
    SELECT u.name, o.product, o.amount
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    UNION
    SELECT u.name, o.product, o.amount
    FROM orders o
    LEFT JOIN users u ON o.user_id = u.id
    WHERE u.id IS NULL
''')
for name, product, amount in cursor.fetchall():
    if product:
        print(f"  {name}: {product} (${amount:.2f})")
    else:
        print(f"  {name}: (no orders)")
print()

```

    INNER JOIN - Users and their orders:
      Alice Johnson: Laptop ($999.99)
      Alice Johnson: Mouse ($29.99)
      Alice Johnson: Laptop ($999.99)
      Alice Johnson: Mouse ($29.99)
      Bob Smith: Monitor ($299.99)
      Bob Smith: USB Cable ($9.99)
      Bob Smith: Monitor ($299.99)
      Bob Smith: USB Cable ($9.99)
      Carol White: Keyboard ($79.99)
      Carol White: Keyboard ($79.99)
      David Brown: Headphones ($149.99)
      David Brown: Headphones ($149.99)
    
    LEFT JOIN - All users with their order count:
      Alice Johnson: 4 orders
      Bob Smith: 4 orders
      Carol White: 2 orders
      David Brown: 2 orders
    
    RIGHT JOIN (simulated) - All orders with user info:
      David Brown: Headphones ($149.99)
      David Brown: Headphones ($149.99)
      Carol White: Keyboard ($79.99)
      Carol White: Keyboard ($79.99)
      Alice Johnson: Laptop ($999.99)
      Alice Johnson: Laptop ($999.99)
      Bob Smith: Monitor ($299.99)
      Bob Smith: Monitor ($299.99)
      Alice Johnson: Mouse ($29.99)
      Alice Johnson: Mouse ($29.99)
      Bob Smith: USB Cable ($9.99)
      Bob Smith: USB Cable ($9.99)
    
    FULL OUTER JOIN (simulated with UNION) - All users and orders:
      Alice Johnson: Laptop ($999.99)
      Alice Johnson: Mouse ($29.99)
      Bob Smith: Monitor ($299.99)
      Bob Smith: USB Cable ($9.99)
      Carol White: Keyboard ($79.99)
      David Brown: Headphones ($149.99)
    


### Use `UPDATE` to modify data

`UPDATE` modifies existing records in a table. Because this operation changes data, it should be performed within a transaction. **Always use a `WHERE` clause to target specific rows.**

*Update examples*


```python
# Update single column
with conn:
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users
            SET age = 29
            WHERE name = 'Alice Johnson'
        ''')
    except sqlite3.DatabaseError as e:
        print(f"Database error occurred during update: {e}")
    

cursor.execute('SELECT name, age FROM users WHERE name = "Alice Johnson"')
print("After update:", cursor.fetchone())
print()

# Update multiple columns
with conn:
    try:
        ids_to_update = (2, 3)  # Bob Smith and Carol White
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users
            SET age = 36
            WHERE id IN (?, ?)
        ''', ids_to_update)
    except sqlite3.DatabaseError as e:
        print(f"Database error occurred during update: {e}")

cursor.execute('SELECT name, age, email FROM users WHERE age = 36')
print("Multiple columns updated:", cursor.fetchall())
print()

# Update with calculation
try:
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users
        SET age = age + 1
        WHERE age < 35
    ''')
except sqlite3.DatabaseError as e:
    print(f"Database error occurred during update: {e}")
    
print("Ages increased for users under 35:")
cursor.execute('SELECT name, age FROM users ORDER BY name')
for name, age in cursor.fetchall():
    print(f"  {name}: {age}")
```

    After update: ('Alice Johnson', 29)
    
    Multiple columns updated: [('Bob Smith', 36, 'bob.smith@example.com'), ('Carol White', 36, 'carol@example.com')]
    
    Ages increased for users under 35:
      Alice Johnson: 30
      Bob Smith: 36
      Carol White: 36
      David Brown: 35


### Use `DELETE` to remove data

`DELETE` removes records from a table. **Always use a `WHERE` clause to target specific rows; otherwise, all rows will be deleted.** Deletion operations should be performed within a transaction.


```python
# Delete single row
print(f"Orders before delete: {cursor.execute('SELECT COUNT(*) FROM orders').fetchone()[0]}")

with conn:
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM orders WHERE id = 1')
    except sqlite3.DatabaseError as e:
        print(f"Database error occurred during delete: {e}")

print(f"Orders after delete: {cursor.execute('SELECT COUNT(*) FROM orders').fetchone()[0]}")
print()

# Delete multiple rows with condition
with conn:
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM orders WHERE amount < 20')
    except sqlite3.DatabaseError as e:
        print(f"Database error occurred during delete: {e}")

print("Remaining orders (after deleting items < $20):")
cursor.execute('SELECT user_id, product, amount FROM orders ORDER BY user_id')
for user_id, product, amount in cursor.fetchall():
    print(f"  User {user_id}: {product} - ${amount:.2f}")
```

    Orders before delete: 12
    Orders after delete: 11
    
    Remaining orders (after deleting items < $20):
      User 1: Mouse - $29.99
      User 1: Laptop - $999.99
      User 1: Mouse - $29.99
      User 2: Monitor - $299.99
      User 2: Monitor - $299.99
      User 3: Keyboard - $79.99
      User 3: Keyboard - $79.99
      User 4: Headphones - $149.99
      User 4: Headphones - $149.99


### Advanced queries

This section introduces common SQL operators and patterns for constructing more complex queries.

*`AND`, `OR`, `IN`, `BETWEEN`, and `LIKE` operators*


```python
# WHERE with AND, OR
print("WHERE with AND/OR:")
cursor.execute('''
    SELECT name, age FROM users
    WHERE age > 30 AND name LIKE 'B%'
''')
print(f"  Users over 30 with names starting with B: {cursor.fetchall()}")
print()

# IN operator
print("IN operator:")
cursor.execute('''
    SELECT name FROM users
    WHERE id IN (1, 3, 4)
''')
for (name,) in cursor.fetchall():
    print(f"  {name}")
print()

# BETWEEN
print("BETWEEN operator:")
cursor.execute('''
    SELECT name, age FROM users
    WHERE age BETWEEN 30 AND 40
''')
for name, age in cursor.fetchall():
    print(f"  {name}: {age}")
print()

# LIKE operator (pattern matching)
print("LIKE operator (pattern matching):")
cursor.execute('''
    SELECT name, email FROM users
    WHERE email LIKE '%@example.com'
''')
for name, email in cursor.fetchall():
    print(f"  {name}: {email}")
print()
```

    WHERE with AND/OR:
      Users over 30 with names starting with B: [('Bob Smith', 36)]
    
    IN operator:
      Alice Johnson
      Carol White
      David Brown
    
    BETWEEN operator:
      Alice Johnson: 30
      Bob Smith: 36
      Carol White: 36
      David Brown: 35
    
    LIKE operator (pattern matching):
      Alice Johnson: alice@example.com
      Bob Smith: bob.smith@example.com
      Carol White: carol@example.com
      David Brown: david@example.com
    


*`IS NULL`, `UNION`, and subqueries in `WHERE` clauses*


```python
# IS NULL / IS NOT NULL
print("NULL handling:")
with conn:
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (name, age) VALUES ('Eve Davis', 25)
        ''')
    except sqlite3.DatabaseError as e:
        print(f"Database error occurred during insert: {e}")


cursor.execute('SELECT name, email FROM users WHERE email IS NULL')
print(f"  Users without email: {cursor.fetchall()}")
print()

# UNION - combine results from multiple queries
print("UNION - combining results:")
cursor.execute('''
    SELECT 'User' as type, name FROM users WHERE age > 35
    UNION
    SELECT 'Young User', name FROM users WHERE age < 30
''')
for row_type, name in cursor.fetchall():
    print(f"  {row_type}: {name}")
print()

# Subquery in WHERE
print("Subquery in WHERE:")
cursor.execute('''
    SELECT name FROM users
    WHERE id IN (
        SELECT DISTINCT user_id FROM orders
    )
''')
print("  Users with orders:", [row[0] for row in cursor.fetchall()])
```

    NULL handling:
      Users without email: [('Eve Davis', None)]
    
    UNION - combining results:
      User: Bob Smith
      User: Carol White
      Young User: Eve Davis
    
    Subquery in WHERE:
      Users with orders: ['Alice Johnson', 'Bob Smith', 'Carol White', 'David Brown']


### Best practices

- **Prevent SQL injection**

  Always use **parameterised queries** with `?` placeholders:

  ```python
  # SAFE: parameterised query
  cursor.execute('SELECT * FROM users WHERE name = ?', (user_name,))

  # UNSAFE: string concatenation
  cursor.execute(f"SELECT * FROM users WHERE name = '{user_name}'")
  ```

- **Manage transactions**

  Use transactions to maintain data consistency:

  ```python
  try:
      cursor.execute('INSERT ...')
      cursor.execute('UPDATE ...')
      conn.commit()  # Commit only if all operations succeed
  except Exception as e:
      conn.rollback()  # Undo changes if an error occurs
      print(f"Error: {e}")
  ```

- **Manage connections**

  Use a context manager for automatic resource management:

  ```python
  with sqlite3.connect('database.db') as conn:
      cursor = conn.cursor()
      cursor.execute('SELECT * FROM users')
      # The connection is closed automatically
  ```

### Common patterns


```python
# Pattern 1: Search with LIKE
def search_users(search_term):
    cursor.execute('''
        SELECT id, name, email FROM users
        WHERE name LIKE ? OR email LIKE ?
    ''', (f'%{search_term}%', f'%{search_term}%'))
    return cursor.fetchall()

print("Search results for 'a':")
for user_id, name, email in search_users('a'):
    print(f"  {name} ({email})")
print()

# Pattern 2: Pagination
def paginate(table, page=1, per_page=2):
    offset = (page - 1) * per_page
    cursor.execute(f'''
        SELECT * FROM {table}
        LIMIT ? OFFSET ?
    ''', (per_page, offset))
    return cursor.fetchall()

print("Page 2 of users (2 per page):")
for row in paginate('users', page=2, per_page=2):
    print(f"  {row}")
print()

# Pattern 3: Check if record exists
def user_exists(user_id):
    cursor.execute('SELECT 1 FROM users WHERE id = ?', (user_id,))
    return cursor.fetchone() is not None

print(f"User ID 1 exists: {user_exists(1)}")
print(f"User ID 999 exists: {user_exists(999)}")
print()

# Pattern 4: Last inserted ID
cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Helen Moore', 27))
conn.commit()
last_id = cursor.lastrowid
print(f"Last inserted user ID: {last_id}")

cursor.close()
conn.close()
```

    Search results for 'a':
      Alice Johnson (alice@example.com)
      Bob Smith (bob.smith@example.com)
      Carol White (carol@example.com)
      David Brown (david@example.com)
      Eve Davis (None)
    
    Page 2 of users (2 per page):
      (3, 'Carol White', 'carol@example.com', 36, '2026-08-14 11:46:25')
      (4, 'David Brown', 'david@example.com', 35, '2026-08-14 11:46:25')
    
    User ID 1 exists: True
    User ID 999 exists: False
    
    Last inserted user ID: 6


## Conclusion

SQLite is a lightweight yet powerful database solution that brings relational database capabilities to Python projects without the operational overhead of a separate database server. This article has demonstrated how to create a database, define tables, insert and query data, and use joins, transactions, and constraints to maintain reliable and consistent records. It has also introduced practical patterns such as parameterised queries, filtering, aggregation, and safe data modification, all of which are essential in real-world applications.

SQLite is particularly useful because of its simplicity. It is easy to set up, works well for local applications, prototypes, embedded systems, and smaller data-driven projects, and integrates naturally with Python. Nevertheless, it has limitations. SQLite is best suited to lightweight workloads and is not the ideal choice for high-concurrency, multi-user systems, for which a client-server database would be more appropriate.

Overall, SQLite is an excellent choice when a Python application requires a fast, portable, and dependable database. Once the core concepts covered in this article are understood, it becomes straightforward to build more complex data models and maintain clear, efficient database logic.

Did this article help you ? Let me know in the comments below, and don't forget to drop a like if you enjoyed the read! Thank you.
