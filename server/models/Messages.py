"""MongoDB Message model."""

from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic."""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class Message(BaseModel):
    """Message model."""
    
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    source: Optional[str] = None
    author: Optional[str] = None
    content: Optional[str] = None
    hash: Optional[str] = None

    class Config:
        """Pydantic config."""
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "source": "discord",
                "author": "username",
                "content": "message content",
                "hash": "abc123..."
            }
        }
