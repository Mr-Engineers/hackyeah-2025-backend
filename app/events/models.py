from pydantic import BaseModel, Field
from typing import List, Optional

class BadEvent():
    title: str
    description: str
    image: str
    decisive_atribute: str
    decreased_attribute: str
    decrease_value: int

