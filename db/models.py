from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class Market(BaseModel):
    id: str
    title: str
    description: str
    vertical: str
    resolution_criteria: str
    source_of_truth: str
    probability_yes: float
    probability_updated_at: Optional[datetime] = None
    status: str
    outcome: Optional[str] = None
    closes_at: datetime
    resolved_at: Optional[datetime] = None
    created_by: str
    total_yes_usdc: float
    total_no_usdc: float
    created_at: datetime

    @property
    def total_volume_usdc(self) -> float:
        return self.total_yes_usdc + self.total_no_usdc
    
    @property
    def probability_no(self) -> float:
        return 1.0 - self.probability_yes
