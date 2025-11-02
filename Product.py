from dataclasses import dataclass, asdict

@dataclass
class Product:
    id: int              ### Unique product identifier
    name: str            ### Product name
    price: float         ### Product price

    def to_dict(self):
        ### Converts Product dataclass to dictionary
        return asdict(self)
