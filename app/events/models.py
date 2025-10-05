from pydantic import BaseModel, Field
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class BadEvent():
    title: str
    description: str
    category: str
    decisive_atribute: str
    threshold: float
    decreased_attribute: list[str]
    decrease_value: list[float]

    def __str__(self):
        return (
            f"BadEvent(\n"
            f"  Title: {self.title}\n"
            f"  Description: {self.description}\n"
            f"  category: {self.category}\n"
            f"  Decisive attribute: {self.decisive_atribute}\n"
            f"  Decisive threshold: {self.threshold}\n"
            f"  Decreased attribute: {self.decreased_attribute}\n"
            f"  Decrease value: {self.decrease_value}\n"
            f")"
        )
    
    def get_decreased_attribute_dict(self):
        return dict(zip(self.decreased_attribute, self.decrease_value))


@dataclass
class Event:
    title: str
    description: str
    category: str

    required_attributes: list[str]
    required_attribute_values: list[float]

    advantaged_attributes: list[str]
    advantaged_attribute_values: list[float]

    disadvantaged_attributes: list[str]
    disadvantaged_attribute_values: list[float]

    job_name: str
    chance_increaser: int

    def __str__(self) -> str:
        return (
            f"Event(title='{self.title}', job='{self.job_name}')\n"
            f"Description: {self.description}\n"
            f"category: {self.category}\n\n"
            f"Required:\n"
            f"  {dict(zip(self.required_attributes, self.required_attribute_values))}\n"
            f"Advantaged:\n"
            f"  {dict(zip(self.advantaged_attributes, self.advantaged_attribute_values))}\n"
            f"Disadvantaged:\n"
            f"  {dict(zip(self.disadvantaged_attributes, self.disadvantaged_attribute_values))}\n"
            f"Chance job_name: {self.job_name}\n"
            f"Chance Increaser: {self.chance_increaser}\n\n"
        )
    
    def get_required_attributes_dict(self):
        return dict(zip(self.required_attributes, self.required_attribute_values))
        
    def get_advantaged_attributes_dict(self):
        return dict(zip(self.advantaged_attributes, self.advantaged_attribute_values))
    
    def get_disadvantaged_attributes_dict(self):
        return dict(zip(self.disadvantaged_attributes, self.disadvantaged_attribute_values))

