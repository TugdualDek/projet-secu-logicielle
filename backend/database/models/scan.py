from dataclasses import dataclass
from datetime import datetime

@dataclass
class Scan:
    id: int
    target_url: str
    status: str
    created_at: datetime
    completed_at: datetime = None
    
    @classmethod
    def from_db_row(cls, row):
        return cls(
            id=row[0],
            target_url=row[1],
            status=row[2],
            created_at=row[3],
            completed_at=row[4]
        )
