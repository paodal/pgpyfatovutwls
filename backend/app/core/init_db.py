import asyncio
from tortoise import Tortoise
from passlib.context import CryptContext
import structlog

from .config import settings, TORTOISE_ORM
from ..models.user import User
from ..models.subscription import SubscriptionPlan

logger = structlog.get_logger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def init_db():
    """Initialize database with default data"""
    logger.info("Initializing database...")
    
    # Initialize Tortoise
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    
    # Create super admin if not exists
    await create_super_admin()
    
    # Create default subscription plans
    await create_default_plans()
    
    logger.info("Database initialization completed")


async def create_super_admin():
    """Create super admin user if not exists"""
    admin_email = settings.SUPER_ADMIN_EMAIL
    
    try:
        # Check if super admin already exists
        admin = await User.filter(email=admin_email).first()
        
        if not admin:
            # Create super admin
            hashed_password = pwd_context.hash("admin123")  # Default password
            
            admin = await User.create(
                email=admin_email,
                full_name="Super Administrator",
                hashed_password=hashed_password,
                is_active=True,
                is_superuser=True,
                language="it",
                timezone="Europe/Rome"
            )
            
            logger.info(f"Super admin created: {admin_email}")
            logger.info("Default password: admin123 (change it after first login)")
        else:
            # Ensure existing user is super admin
            if not admin.is_superuser:
                admin.is_superuser = True
                await admin.save()
                logger.info(f"Updated {admin_email} to super admin")
            else:
                logger.info(f"Super admin already exists: {admin_email}")
                
    except Exception as e:
        logger.error(f"Error creating super admin: {e}")


async def create_default_plans():
    """Create default subscription plans if they don't exist"""
    try:
        # Check if plans already exist
        plan_count = await SubscriptionPlan.all().count()
        
        if plan_count == 0:
            # Create Free plan
            await SubscriptionPlan.create(
                name="Free",
                plan_type="free",
                price=0.00,
                currency_code="EUR",
                billing_period_days=30,
                max_projects=1,
                max_storage_gb=1,
                has_priority_support=False,
                has_advanced_features=False,
                is_active=True,
                lemon_squeezy_product_id=None,
                lemon_squeezy_variant_id=None
            )
            
            # Create Premium plan  
            await SubscriptionPlan.create(
                name="Premium",
                plan_type="premium",
                price=29.00,
                currency_code="EUR", 
                billing_period_days=30,
                max_projects=10,
                max_storage_gb=50,
                has_priority_support=True,
                has_advanced_features=True,
                is_active=True,
                lemon_squeezy_product_id="test_product_123",  # Test IDs for development
                lemon_squeezy_variant_id="test_variant_456"
            )
            
            logger.info("Default subscription plans created")
        else:
            logger.info("Subscription plans already exist")
            
    except Exception as e:
        logger.error(f"Error creating subscription plans: {e}")


async def close_db():
    """Close database connections"""
    await Tortoise.close_connections()


if __name__ == "__main__":
    # Allow running this script directly for manual initialization
    asyncio.run(init_db())
    asyncio.run(close_db())