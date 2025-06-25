from tortoise.models import Model
from tortoise import fields
from datetime import datetime
from typing import Optional


class BaseModel(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
    def to_dict(self) -> dict:
        """Convert model instance to dictionary"""
        result = {}
        for field_name, field_obj in self._meta.fields_map.items():
            value = getattr(self, field_name)
            if isinstance(value, datetime):
                result[field_name] = value.isoformat()
            elif hasattr(value, 'to_dict'):
                result[field_name] = value.to_dict()
            else:
                result[field_name] = value
        return result