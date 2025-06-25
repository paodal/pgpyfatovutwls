from tortoise import fields
from .base import BaseModel
from passlib.context import CryptContext
from typing import Optional


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    email = fields.CharField(max_length=255, unique=True, index=True)
    full_name = fields.CharField(max_length=255, null=True)
    hashed_password = fields.CharField(max_length=255, null=True)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)
    is_verified = fields.BooleanField(default=False)
    
    # Profile fields
    phone = fields.CharField(max_length=20, null=True)
    language = fields.CharField(max_length=10, default="it")  # ISO 639-1
    timezone = fields.CharField(max_length=50, default="Europe/Rome")
    
    # Lemon Squeezy integration
    lemon_squeezy_customer_id = fields.CharField(max_length=100, null=True, unique=True)
    
    # Relationships
    subscription: fields.ReverseRelation["UserSubscription"]
    
    class Meta:
        table = "users"
        
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @classmethod
    def get_password_hash(cls, password: str) -> str:
        """Generate password hash"""
        return pwd_context.hash(password)
    
    def set_password(self, password: str) -> None:
        """Set user password"""
        self.hashed_password = self.get_password_hash(password)
        
    def check_password(self, password: str) -> bool:
        """Check user password"""
        if not self.hashed_password:
            return False
        return self.verify_password(password, self.hashed_password)
    
    def __str__(self) -> str:
        return f"User(email={self.email})"