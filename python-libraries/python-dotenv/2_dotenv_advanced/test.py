import os

print("variables from .env file:")
print(os.environ.get("APP_ENV"))  # development (example value from .env file)
print(os.environ.get("DB_HOST"))  # localhost (example value from .env file)