from dataclasses import dataclass, asdict

@dataclass
class Product:
    id: int
    name: str
    price: float
    quantity: int = 0  # default = 0

    def to_dict(self):
        return asdict(self)
