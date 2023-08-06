from datetime import date
from typing import Optional

from pydantic import BaseModel

MODEL_TYPE = 'educators_schools'


class APIEducatorsSchoolsFields(BaseModel):
    educator_name: Optional[str] = None
    school_name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    role: Optional[list[str]] = None
    currently_active: Optional[bool] = None
