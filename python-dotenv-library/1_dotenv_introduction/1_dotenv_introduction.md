# Python Dotenv Library Introduction
## What is Dotenv

Dotenv is a lightweight software library for Python and Node.js used by developers to manage application settings, secrets, and credentials outside of their source code. It automatically loads configuration options from a simple text file (usually named .env) and injects them directly into your application's runtime memory. This means Dotenv does not write variables to a permanent system file; it reads key-value pairs from your local text file and injects them into the runtime memory (RAM) of your active application process. In this article, we focus on the Python version.

## How does it work

- **Source File:** It reads your project configuration from a text file (usually named .env)
- **Destination:** It loads these variables into the operating system's process environment. In Python, they are accessed via `os.environ`.
- **Lifespan:** The variables only exist while your application is actively running. Once you stop the server or program, the variables are cleared from memory. This is a significant improvement over storing variables in system files.

## Dotenv Python installation via Terminal
The correct package name is *python-dotenv*; the original project name *dotenv* has been deprecated.
### Using PyPI
    pip install python-dotenv
### Using a specific Python 3 version
    pip3 install python-dotenv
### Using Poetry
    poetry add python-dotenv
### Using UV
    uv pip install python-dotenv

## Verify the installation
We are going to create a quick test script to ensure it is installed correctly.


```python
import os
from dotenv import load_dotenv

# Load the variables from your .env file
load_dotenv()

# Verify by checking your environment path or a specific variable
print("dotenv loaded successfully!")
```

    dotenv loaded successfully!


## Using Dotenv in Python code
Dotenv stores key-value records, and it can automatically recognise string, int, and float variable types. That does not mean you cannot store other types like bool, tuple, list, or dict, but you need to parse key-value pairs and transform them into specific formats. We are going to look at all examples.

### String, Integer and Float variables
#### The .env file
We write variables in the standard way, as we do in Python code.

<pre>APP_ENV="development"
DB_HOST="localhost"
SERVER_PORT=8080
MAX_CONNECTIONS=5
TIMEOUT_LIMIT=4.5
TAX_RATE=0.15</pre>

#### The Python code


```python
import os
from dotenv import load_dotenv

# Load variables into memory
load_dotenv()

# 1. Fetching Strings (No conversion needed)
env_name = os.getenv("APP_ENV")
print(f"Environment: {env_name} (Type: {type(env_name).__name__})")

# 2. Fetching Integers (Convert using int)
port = int(os.getenv("SERVER_PORT"))
print(f"Port: {port} (Type: {type(port).__name__})")

# 3. Fetching Floats (Convert using float)
timeout = float(os.getenv("TIMEOUT_LIMIT"))
print(f"Timeout: {timeout} (Type: {type(timeout).__name__})")
```

    Environment: development (Type: str)
    Port: 8080 (Type: int)
    Timeout: 4.5 (Type: float)


### Boolean variables
We can store boolean values (True/False) in a .env file, but just like numbers, Dotenv reads them strictly as strings ("true" or "false").

We have to convert them to actual booleans in your Python code. The issue is, you cannot use the standard bool() function because Python evaluates any non-empty string as True, even if the value is "False".


```python
value1 = "true"
value2 = "false"
value3 = "1"
value4 = "0"
value5 = ""

print(bool(value1), bool(value2), bool(value3), bool(value4), bool(value5))
```

    True True True True False


#### The .env file
<pre>DEBUG=true
ENABLE_SIGNUPS=false
</pre>

#### The Python code (2 ways to parse)
#### Method A: string comparison<br>
Compare the incoming string directly against "true".


```python
import os
from dotenv import load_dotenv

load_dotenv()

# Lowercase the string to prevent casing issues
is_debug = os.getenv("DEBUG", "false").lower() == "true"
enable_signups = os.getenv("ENABLE_SIGNUPS", "false").lower() == "true"

print(f"Debug mode: {is_debug} (Type: {type(is_debug).__name__})")
print(f"Enable signups: {enable_signups} (Type: {type(enable_signups).__name__})")
```

    Debug mode: True (Type: bool)
    Enable signups: False (Type: bool)


#### Method B: JSON parsing (best for strict validation)
Because "true" and "false" are valid JSON tokens, you can use Python's built-in json.loads() to convert them perfectly.


```python
import os
import json
from dotenv import load_dotenv

load_dotenv()

# json.loads converts "true" to True, and "false" to False
is_debug = json.loads(os.getenv("DEBUG", "false").lower())
enable_signups = json.loads(os.getenv("ENABLE_SIGNUPS", "false").lower())

print(f"Debug mode: {is_debug} (Type: {type(is_debug).__name__})")
print(f"Signups enabled: {enable_signups} (Type: {type(enable_signups).__name__})")
```

    Debug mode: True (Type: bool)
    Signups enabled: False (Type: bool)




### Tuple variables
We have several possibilities for how to store and parse tuple variables in Dotenv.
#### Method A: comma-separated values<br>
Store the items separated by commas. You do not need to include parentheses in the .env file.<br><br>
#### The .env file
<pre>ALLOWED_COLORS="red,green,blue"
DATABASE_COORDINATES="45.12,-122.33"</pre>

#### The Python code


```python
import os
from dotenv import load_dotenv

load_dotenv()

# Parsing a tuple of strings
colors = tuple(os.getenv("ALLOWED_COLORS").split(","))
print(f"colors: {colors} (Type: {type(colors).__name__})")

# Parsing a tuple of floats (using a list comprehension)
coords = tuple(float(x) for x in os.getenv("DATABASE_COORDINATES").split(","))
print(f"coords: {coords} (Type: {type(coords).__name__})")
```

    colors: ('red', 'green', 'blue') (Type: tuple)
    coords: (45.12, -122.33) (Type: tuple)


#### Method B: Literal Evaluation using ast library (best for explicit tuple syntax)

- The .env file
<pre>ADMIN_IDS="(1001, 1002, 1003)"
</pre>

#### The Python code


```python
import os
import ast
from dotenv import load_dotenv

load_dotenv()

# Safely evaluate the string as a Python tuple object
admin_ids = ast.literal_eval(os.getenv("ADMIN_IDS"))

print(f"admin_ids: {admin_ids} (Type: {type(admin_ids).__name__})")
```

    admin_ids: (1001, 1002, 1003) (Type: tuple)


### List variables
We can use exactly the same approaches for list variables.
#### Method A: comma-separated values<br>
Store the items separated by commas. You do not need to include parentheses in the .env file.<br><br>
#### The .env file
<pre>FRUITS="apple,banana,cherry"
PRIME_NUMBERS="2,3,5,7"
</pre>

#### The Python code<br>
Using .split(",") automatically creates a Python list object. You do not need to wrap it in anything extra.


```python
import os
from dotenv import load_dotenv

load_dotenv()

# 1. List of strings
fruit_list = os.getenv("FRUITS").split(",")
print(f"fruit_list: {fruit_list} (Type: {type(fruit_list).__name__})")

# 2. List of integers (using list comprehension)
primes = [int(x) for x in os.getenv("PRIME_NUMBERS").split(",")]
print(f"primes: {primes} (Type: {type(primes).__name__})")
```

    fruit_list: ['apple', 'banana', 'cherry'] (Type: list)
    primes: [2, 3, 5, 7] (Type: list)


#### Method B: Literal evaluation using the ast library (best for explicit list syntax)

#### The .env file
<pre>USER_ROLES='["admin", "editor", "viewer"]'
</pre>

#### The Python code
Use ast.literal_eval() or json.loads(). Both will read the brackets and instantly convert the string into a native Python list.


```python
import os
import ast
import json
from dotenv import load_dotenv

load_dotenv()

# Safely parse the string into a list object using ast.literal_eval
roles = ast.literal_eval(os.getenv("USER_ROLES"))
print(f"roles: {roles} (Type: {type(roles).__name__})")

# Safely parse the string into a list object using json.loads
roles_json = json.loads(os.getenv("USER_ROLES"))
print(f"roles_json: {roles_json} (Type: {type(roles_json).__name__})")

```

    roles: ['admin', 'editor', 'viewer'] (Type: list)
    roles_json: ['admin', 'editor', 'viewer'] (Type: list)


### Dict variables
Let us look at three methods for storing dictionaries in a Dotenv environment.
#### Method A: string parsing using JSON<br>
Store the dictionary as a string in the .env file.<br><br>
#### The .env file for JSON - the dictionary must be in JSON format
<pre>APP_CONFIG_JSON='{"theme": "dark", "retries": 3, "debug": true}'
</pre>

#### The Python code


```python
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Parse the string into a real Python dictionary
config = json.loads(os.getenv("APP_CONFIG_JSON"))

print(f"config: {config} (Type: {type(config).__name__})")
print(f"Theme: {type(config['theme']).__name__}, Retries: {type(config['retries']).__name__}, Debug: {type(config['debug']).__name__}")
```

    config: {'theme': 'dark', 'retries': 3, 'debug': True} (Type: dict)
    Theme: str, Retries: int, Debug: bool


#### Method B: string parsing using Ast library<br>   
#### The .env file for Ast - the dictionary is in native Python format
<pre>APP_CONFIG='{"theme": "dark", "retries": 3, "debug": True}'
</pre>

#### The Python code


```python
import os
import ast
from dotenv import load_dotenv

load_dotenv()

# Safely parse the Python-formatted string into a dict
config = ast.literal_eval(os.getenv("APP_CONFIG"))

print(f"config: {config} (Type: {type(config).__name__})")
print(f"Theme: {type(config['theme']).__name__}, Retries: {type(config['retries']).__name__}, Debug: {type(config['debug']).__name__}")
```

    config: {'theme': 'dark', 'retries': 3, 'debug': True} (Type: dict)
    Theme: str, Retries: int, Debug: bool


#### Method C: using a prefix-based flat structure - best used for simple configurations.
#### The .env file
<pre>DB_HOST="localhost"
DB_PORT=5432
DB_USER="admin"
</pre>

#### The Python code


```python
import os
from dotenv import load_dotenv

load_dotenv()

# Build the dictionary manually
database_config = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)), # Cast to int safely
    "user": os.getenv("DB_USER")
}

print(f"database_config: {database_config} (Type: {type(database_config).__name__})")
print(f"Host: {type(database_config['host']).__name__}, Port: {type(database_config['port']).__name__}, User: {type(database_config['user']).__name__}")
```

    database_config: {'host': 'localhost', 'port': 5432, 'user': 'admin'} (Type: dict)
    Host: str, Port: int, User: str


## Conclusion and recommendations

In this article, we covered the core idea of Dotenv: keep configuration and secrets outside your source code, then load them safely at runtime.

Key takeaways:
- Dotenv reads everything as strings, so explicit parsing is required for `int`, `float`, `bool`, `tuple`, `list`, and `dict` values.
- For structured values, `json.loads()` is a strong default when your `.env` value is valid JSON.
- `ast.literal_eval()` is useful for Python-literal formats, but use it only with trusted input.
- Prefix-based flat keys (like `DB_HOST`, `DB_PORT`) are often the simplest and most maintainable pattern for real projects.

Recommended practice for production:
- Keep `.env` files out of version control (`.gitignore`).
- Store only environment-specific configuration in `.env`, not hardcoded values in application code.
- Define clear defaults and validation in your Python startup logic to avoid runtime surprises.

With these patterns, Dotenv becomes a clean, safe, and scalable way to manage app configuration across local development, staging, and production environments.

Did this help you transition to Dotenv? Let me know in the comments below, and don't forget to drop a like if you enjoyed the read! Thank you.
