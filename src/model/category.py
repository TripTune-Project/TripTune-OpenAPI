from dataclasses import dataclass

@dataclass
class Category:
    category_code: str
    category_name: str
    parent_code: str
    level: int