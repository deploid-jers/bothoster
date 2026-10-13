from pydantic import EmailStr, BaseModel, Field
from typing import List


class EmailSchema(BaseModel):
    email: List[EmailStr]

class RequestConfimEmail(BaseModel):
    token: str = Field(max_length=43)