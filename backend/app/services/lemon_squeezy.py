import httpx
from typing import Optional, Dict, Any
from ..core.config import settings
import structlog

logger = structlog.get_logger(__name__)


class LemonSqueezy:
    """Lemon Squeezy API client"""
    
    def __init__(self):
        self.api_key = settings.LEMON_SQUEEZY_API_KEY
        self.base_url = "https://api.lemonsqueezy.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json",
        }
    
    async def get_customer(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """Get customer by ID"""
        if not self.api_key:
            logger.warning("Lemon Squeezy API key not configured")
            return None
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/customers/{customer_id}",
                    headers=self.headers
                )
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f"Failed to get customer: {response.status_code}")
                    return None
        except Exception as e:
            logger.error(f"Error getting customer: {e}")
            return None
    
    async def create_checkout(
        self, 
        variant_id: str, 
        user_email: str,
        custom_data: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Create checkout session"""
        
        # Return mock data for test variant IDs
        if variant_id.startswith("test_"):
            logger.info(f"Using test variant ID: {variant_id}")
            return {
                "data": {
                    "type": "checkouts",
                    "attributes": {
                        "url": f"https://test-checkout-url.com?variant={variant_id}&email={user_email}"
                    }
                }
            }
        
        if not self.api_key:
            logger.warning("Lemon Squeezy API key not configured")
            return None
            
        checkout_data = {
            "data": {
                "type": "checkouts",
                "attributes": {
                    "checkout_data": {
                        "email": user_email,
                        "custom": custom_data or {}
                    }
                },
                "relationships": {
                    "store": {
                        "data": {
                            "type": "stores",
                            "id": settings.LEMON_SQUEEZY_STORE_ID
                        }
                    },
                    "variant": {
                        "data": {
                            "type": "variants", 
                            "id": variant_id
                        }
                    }
                }
            }
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/checkouts",
                    json=checkout_data,
                    headers=self.headers
                )
                if response.status_code == 201:
                    return response.json()
                else:
                    logger.error(f"Failed to create checkout: {response.status_code}")
                    return None
        except Exception as e:
            logger.error(f"Error creating checkout: {e}")
            return None
    
    async def get_subscription(self, subscription_id: str) -> Optional[Dict[str, Any]]:
        """Get subscription by ID"""
        if not self.api_key:
            logger.warning("Lemon Squeezy API key not configured")
            return None
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/subscriptions/{subscription_id}",
                    headers=self.headers
                )
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f"Failed to get subscription: {response.status_code}")
                    return None
        except Exception as e:
            logger.error(f"Error getting subscription: {e}")
            return None
    
    async def cancel_subscription(self, subscription_id: str) -> bool:
        """Cancel subscription"""
        if not self.api_key:
            logger.warning("Lemon Squeezy API key not configured")
            return False
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{self.base_url}/subscriptions/{subscription_id}",
                    headers=self.headers
                )
                return response.status_code == 204
        except Exception as e:
            logger.error(f"Error cancelling subscription: {e}")
            return False


lemon_squeezy = LemonSqueezy()