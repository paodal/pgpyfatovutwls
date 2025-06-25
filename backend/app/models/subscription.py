from tortoise import fields
from .base import BaseModel
from decimal import Decimal
from enum import Enum


class PlanType(str, Enum):
    FREE = "free"
    PREMIUM = "premium"


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive" 
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    PAUSED = "paused"


class CurrencyCode(str, Enum):
    EUR = "EUR"
    USD = "USD" 
    GBP = "GBP"


class SubscriptionPlan(BaseModel):
    name = fields.CharField(max_length=100)
    plan_type = fields.CharEnumField(PlanType, default=PlanType.FREE)
    price = fields.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    currency_code = fields.CharEnumField(CurrencyCode, default=CurrencyCode.EUR)
    billing_period_days = fields.IntField(default=30)  # Monthly by default
    
    # Features
    max_projects = fields.IntField(default=1)
    max_storage_gb = fields.IntField(default=1)
    has_priority_support = fields.BooleanField(default=False)
    has_advanced_features = fields.BooleanField(default=False)
    
    # Lemon Squeezy integration
    lemon_squeezy_product_id = fields.CharField(max_length=100, null=True)
    lemon_squeezy_variant_id = fields.CharField(max_length=100, null=True)
    
    is_active = fields.BooleanField(default=True)
    
    # Relationships
    user_subscriptions: fields.ReverseRelation["UserSubscription"]
    
    class Meta:
        table = "subscription_plans"
        
    def __str__(self) -> str:
        return f"SubscriptionPlan(name={self.name}, type={self.plan_type})"


class UserSubscription(BaseModel):
    user = fields.ForeignKeyField("models.User", related_name="subscription")
    plan = fields.ForeignKeyField("models.SubscriptionPlan", related_name="user_subscriptions")
    
    status = fields.CharEnumField(SubscriptionStatus, default=SubscriptionStatus.ACTIVE)
    starts_at = fields.DatetimeField()
    ends_at = fields.DatetimeField(null=True)
    cancelled_at = fields.DatetimeField(null=True)
    
    # Lemon Squeezy integration
    lemon_squeezy_subscription_id = fields.CharField(max_length=100, null=True, unique=True)
    lemon_squeezy_order_id = fields.CharField(max_length=100, null=True)
    
    # Billing
    billing_period_starts_at = fields.DatetimeField(null=True)
    billing_period_ends_at = fields.DatetimeField(null=True)
    
    class Meta:
        table = "user_subscriptions"
        unique_together = [("user", "plan")]
        
    def is_active(self) -> bool:
        """Check if subscription is currently active"""
        return self.status == SubscriptionStatus.ACTIVE
    
    def __str__(self) -> str:
        return f"UserSubscription(user={self.user.email}, plan={self.plan.name}, status={self.status})"