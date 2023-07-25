from pydantic import BaseModel
import uuid


# PhoneNumber entity - Shared properties
class PhoneNumberBase(BaseModel):
    athlete_id           : uuid.UUID | None = None
    fcenter_id           : uuid.UUID | None = None
    country_code_id      : str
    phone_number         : str 
    

# PhoneNumber entity - Properties to receive via API on creation or update
class PhoneNumberSchemaIn(PhoneNumberBase):
    id                   : int | None = None


# PhoneNumber - Schema for DB
class PhoneNumberInDBBase(PhoneNumberBase):
    id                   : int
    class Config:
        orm_mode = True


class PhoneNumber(PhoneNumberInDBBase):
    pass
