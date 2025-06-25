from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from ..auth.dependencies import get_current_active_user
from ..models.user import User
from ..models.subscription import SubscriptionPlan, UserSubscription, PlanType, CurrencyCode
from ..services.lemon_squeezy import lemon_squeezy
from ..services.email import email_service
import structlog

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


class SubscriptionPlanResponse(BaseModel):
    id: int
    name: str
    plan_type: PlanType
    price: float
    currency_code: CurrencyCode
    billing_period_days: int
    max_projects: int
    max_storage_gb: int
    has_priority_support: bool
    has_advanced_features: bool
    is_active: bool
    
    class Config:
        from_attributes = True


class CheckoutResponse(BaseModel):
    checkout_url: str


@router.get("/plans", response_model=List[SubscriptionPlanResponse])
async def get_subscription_plans():
    """Get all active subscription plans"""
    plans = await SubscriptionPlan.filter(is_active=True).all()
    return [SubscriptionPlanResponse.from_orm(plan) for plan in plans]


@router.post("/checkout/{plan_id}", response_model=CheckoutResponse)
async def create_checkout(
    plan_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """Create checkout session for subscription plan"""
    plan = await SubscriptionPlan.get_or_none(id=plan_id, is_active=True)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription plan not found"
        )
    
    # Check if plan is free
    if plan.plan_type == PlanType.FREE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create checkout for free plan"
        )
    
    # Check if user already has an active subscription for this plan
    existing_subscription = await UserSubscription.filter(
        user=current_user,
        plan=plan,
        status="active"
    ).first()
    
    if existing_subscription:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has active subscription for this plan"
        )
    
    if not plan.lemon_squeezy_variant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Plan not configured for checkout"
        )
    
    # Create checkout with Lemon Squeezy
    checkout_data = await lemon_squeezy.create_checkout(
        variant_id=plan.lemon_squeezy_variant_id,
        user_email=current_user.email,
        custom_data={
            "user_id": current_user.id,
            "plan_id": plan.id
        }
    )
    
    if not checkout_data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create checkout session"
        )
    
    checkout_url = checkout_data["data"]["attributes"]["url"]
    return CheckoutResponse(checkout_url=checkout_url)


@router.get("/current")
async def get_current_subscription(
    current_user: User = Depends(get_current_active_user)
):
    """Get user's current subscription"""
    subscription = await UserSubscription.filter(
        user=current_user,
        status="active"
    ).prefetch_related("plan").first()
    
    if not subscription:
        # Return free plan if no active subscription
        free_plan = await SubscriptionPlan.filter(plan_type=PlanType.FREE).first()
        return {
            "plan": SubscriptionPlanResponse.from_orm(free_plan) if free_plan else None,
            "status": "free",
            "subscription": None
        }
    
    return {
        "plan": SubscriptionPlanResponse.from_orm(subscription.plan),
        "status": subscription.status,
        "subscription": {
            "id": subscription.id,
            "starts_at": subscription.starts_at,
            "ends_at": subscription.ends_at,
            "billing_period_starts_at": subscription.billing_period_starts_at,
            "billing_period_ends_at": subscription.billing_period_ends_at
        }
    }


@router.post("/cancel/{subscription_id}")
async def cancel_subscription(
    subscription_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """Cancel user subscription"""
    subscription = await UserSubscription.filter(
        id=subscription_id,
        user=current_user
    ).prefetch_related("plan").first()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    
    if subscription.lemon_squeezy_subscription_id:
        # Cancel with Lemon Squeezy
        success = await lemon_squeezy.cancel_subscription(
            subscription.lemon_squeezy_subscription_id
        )
        if not success:
            logger.error(f"Failed to cancel subscription {subscription_id} with Lemon Squeezy")
    
    # Update local subscription status
    subscription.status = "cancelled"
    await subscription.save()
    
    return {"message": "Subscription cancelled successfully"}