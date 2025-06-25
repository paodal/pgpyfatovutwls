from fastapi import APIRouter, Request, HTTPException, status
from ..models.user import User
from ..models.subscription import UserSubscription, SubscriptionPlan, SubscriptionStatus
from ..services.email import email_service
from ..core.config import settings
import json
import hmac
import hashlib
from datetime import datetime
import structlog

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """Verify Lemon Squeezy webhook signature"""
    if not settings.LEMON_SQUEEZY_WEBHOOK_SECRET:
        logger.warning("Webhook secret not configured")
        return False
    
    expected_signature = hmac.new(
        settings.LEMON_SQUEEZY_WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected_signature}", signature)


@router.post("/lemon-squeezy")
async def lemon_squeezy_webhook(request: Request):
    """Handle Lemon Squeezy webhooks"""
    payload = await request.body()
    signature = request.headers.get("x-signature", "")
    
    if not verify_webhook_signature(payload, signature):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid webhook signature"
        )
    
    try:
        data = json.loads(payload.decode())
        event_name = data.get("meta", {}).get("event_name")
        
        logger.info(f"Received Lemon Squeezy webhook: {event_name}")
        
        if event_name == "subscription_created":
            await handle_subscription_created(data)
        elif event_name == "subscription_updated":
            await handle_subscription_updated(data)
        elif event_name == "subscription_cancelled":
            await handle_subscription_cancelled(data)
        elif event_name == "subscription_expired":
            await handle_subscription_expired(data)
        else:
            logger.info(f"Unhandled webhook event: {event_name}")
        
        return {"status": "success"}
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing webhook"
        )


async def handle_subscription_created(data: dict):
    """Handle subscription created webhook"""
    subscription_data = data["data"]
    attributes = subscription_data["attributes"]
    
    # Extract custom data
    custom_data = attributes.get("custom_data", {})
    user_id = custom_data.get("user_id")
    plan_id = custom_data.get("plan_id")
    
    if not user_id or not plan_id:
        logger.error("Missing user_id or plan_id in webhook data")
        return
    
    # Get user and plan
    user = await User.get_or_none(id=user_id)
    plan = await SubscriptionPlan.get_or_none(id=plan_id)
    
    if not user or not plan:
        logger.error(f"User or plan not found: user_id={user_id}, plan_id={plan_id}")
        return
    
    # Create subscription
    subscription = await UserSubscription.create(
        user=user,
        plan=plan,
        status=SubscriptionStatus.ACTIVE,
        lemon_squeezy_subscription_id=subscription_data["id"],
        starts_at=datetime.fromisoformat(attributes["starts_at"].replace("Z", "+00:00")),
        ends_at=datetime.fromisoformat(attributes["ends_at"].replace("Z", "+00:00")) if attributes.get("ends_at") else None,
        billing_period_starts_at=datetime.fromisoformat(attributes["billing_anchor"].replace("Z", "+00:00")),
    )
    
    # Send confirmation email
    try:
        await email_service.send_subscription_confirmation(
            user.email, 
            user.full_name, 
            plan.name
        )
    except Exception as e:
        logger.warning(f"Failed to send subscription confirmation email: {e}")
    
    logger.info(f"Subscription created for user {user.email}")


async def handle_subscription_updated(data: dict):
    """Handle subscription updated webhook"""
    subscription_data = data["data"]
    attributes = subscription_data["attributes"]
    
    # Find existing subscription
    subscription = await UserSubscription.filter(
        lemon_squeezy_subscription_id=subscription_data["id"]
    ).first()
    
    if not subscription:
        logger.error(f"Subscription not found: {subscription_data['id']}")
        return
    
    # Update subscription
    subscription.status = attributes["status"]
    subscription.ends_at = datetime.fromisoformat(attributes["ends_at"].replace("Z", "+00:00")) if attributes.get("ends_at") else None
    await subscription.save()
    
    logger.info(f"Subscription updated: {subscription_data['id']}")


async def handle_subscription_cancelled(data: dict):
    """Handle subscription cancelled webhook"""
    subscription_data = data["data"]
    attributes = subscription_data["attributes"]
    
    # Find existing subscription
    subscription = await UserSubscription.filter(
        lemon_squeezy_subscription_id=subscription_data["id"]
    ).first()
    
    if not subscription:
        logger.error(f"Subscription not found: {subscription_data['id']}")
        return
    
    # Update subscription
    subscription.status = SubscriptionStatus.CANCELLED
    subscription.cancelled_at = datetime.fromisoformat(attributes["cancelled_at"].replace("Z", "+00:00"))
    await subscription.save()
    
    logger.info(f"Subscription cancelled: {subscription_data['id']}")


async def handle_subscription_expired(data: dict):
    """Handle subscription expired webhook"""
    subscription_data = data["data"]
    
    # Find existing subscription
    subscription = await UserSubscription.filter(
        lemon_squeezy_subscription_id=subscription_data["id"]
    ).first()
    
    if not subscription:
        logger.error(f"Subscription not found: {subscription_data['id']}")
        return
    
    # Update subscription
    subscription.status = SubscriptionStatus.EXPIRED
    await subscription.save()
    
    logger.info(f"Subscription expired: {subscription_data['id']}")