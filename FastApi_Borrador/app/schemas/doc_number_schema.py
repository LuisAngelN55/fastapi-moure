from pydantic import BaseModel
import uuid


# PhoneNumber entity - Shared properties
class DocNumberBase(BaseModel):
    athlete_id           : uuid.UUID | None = None
    fcenter_id           : uuid.UUID | None = None
    doc_type_code        : str
    doc_number           : str
    

# PhoneNumber entity - Properties to receive via API on creation or update
class DocNumberSchemaIn(DocNumberBase):
    id                   : int | None = None


# PhoneNumber - Schema for DB
class DocNumberInDBBase(DocNumberBase):
    id                   : int
    class Config:
        orm_mode = True


class DocNumber(DocNumberInDBBase):
    pass
