from typing import Optional
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    email: str
    age: Optional[int] = Field(default=None) # Added a new column
    new_column: Optional[str] = Field(default=None) # Added a new column
    