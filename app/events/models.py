from pydantic import BaseModel, Field
from typing import List, Optional

class BadEvent():
    title: str
    description: str
    image: str
    decisive_atribute: str
    decreased_attribute: str
    decrease_value: int

    def __str__(self):
        return (
            f"BadEvent(\n"
            f"  Title: {self.title}\n"
            f"  Description: {self.description}\n"
            f"  Image: {self.image}\n"
            f"  Decisive attribute: {self.decisive_atribute}\n"
            f"  Decreased attribute: {self.decreased_attribute}\n"
            f"  Decrease value: {self.decrease_value}\n"
            f")"
        )