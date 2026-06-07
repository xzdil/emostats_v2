from pydantic import BaseModel, Field, ConfigDict, validator
from typing import List, Optional   
from datetime import date
from datetime import datetime

# Base model with ORM mode enabled
class BaseValidateModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
