from typing import Optional
from sqlmodel import Field, SQLModel

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    price: float
    new_column: Optional[str] = Field(default=None) # Added a new column