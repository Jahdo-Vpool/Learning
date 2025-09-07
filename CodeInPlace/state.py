from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class GameState:
    name: str
    country: str
    career: str
    income: float
    rent_expense: float
    savings: float
    month = int = 1
    history: List[Dict[str,Any]] = field(default_factory=list)