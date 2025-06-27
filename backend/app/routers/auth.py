from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from datetime import timedelta
from typing import Optional
from ..auth.jwt import create_access_token
from ..auth.dependencies import get_current_active_user
from ..models.user import User
from ..models.subscription import UserSubscription, SubscriptionPlan
from ..core.config import settings
from ..services.email import email_service
import structlog
from datetime import datetime

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    language: str = "it"


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    is_verified: bool
    is_superuser: bool
    language: str
    
    class Config:
        from_attributes = True


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


class AdminUpdateUserRequest(BaseModel):
    email: str
    full_name: str
    is_superuser: bool = False
    is_active: bool = True


class AdminChangePasswordRequest(BaseModel):
    user_id: int
    new_password: str


class UserSubscriptionResponse(BaseModel):
    id: int
    plan_id: int
    plan_name: str
    status: str
    starts_at: datetime
    ends_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserDetailResponse(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    is_verified: bool
    is_superuser: bool
    language: str
    subscription: Optional[UserSubscriptionResponse] = None
    
    class Config:
        from_attributes = True


class AdminSetSubscriptionRequest(BaseModel):
    user_id: int
    plan_id: int


class AdminCreateUserRequest(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    language: str = "it"
    is_superuser: bool = False


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    """Register new user"""
    # Check if user already exists
    existing_user = await User.filter(email=user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = await User.create(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=User.get_password_hash(user_data.password),
        language=user_data.language,
        is_superuser=(user_data.email == settings.SUPER_ADMIN_EMAIL)
    )
    
    # Send welcome email
    try:
        await email_service.send_welcome_email(user.email, user.full_name)
    except Exception as e:
        logger.warning(f"Failed to send welcome email: {e}")
    
    return UserResponse.from_orm(user)


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login user and return JWT token"""
    user = await User.filter(email=form_data.username).first()
    
    if not user or not user.check_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.from_orm(user)
    )


@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: User = Depends(get_current_active_user)):
    """Get current user profile"""
    return UserResponse.from_orm(current_user)


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: dict,
    current_user: User = Depends(get_current_active_user)
):
    """Update current user profile"""
    allowed_fields = {"full_name", "language", "phone", "timezone"}
    update_data = {k: v for k, v in user_update.items() if k in allowed_fields}
    
    await User.filter(id=current_user.id).update(**update_data)
    updated_user = await User.get(id=current_user.id)
    
    return UserResponse.from_orm(updated_user)


@router.post("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Change current user password"""
    # Verify current password
    if not current_user.check_password(request.current_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    hashed_password = User.get_password_hash(request.new_password)
    await User.filter(id=current_user.id).update(hashed_password=hashed_password)
    
    return {"message": "Password changed successfully"}


@router.get("/users", response_model=list[UserDetailResponse])
async def get_all_users(current_user: User = Depends(get_current_active_user)):
    """Get all users with subscription details (admin only)"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can access this endpoint"
        )
    
    users = await User.all()
    result = []
    
    for user in users:
        # Get user's active subscription
        subscription = await UserSubscription.filter(
            user=user,
            status="active"
        ).select_related('plan').first()
        
        subscription_data = None
        if subscription:
            subscription_data = UserSubscriptionResponse(
                id=subscription.id,
                plan_id=subscription.plan.id,
                plan_name=subscription.plan.name,
                status=subscription.status,
                starts_at=subscription.starts_at,
                ends_at=subscription.ends_at
            )
        
        user_data = UserDetailResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            is_superuser=user.is_superuser,
            language=user.language,
            subscription=subscription_data
        )
        
        result.append(user_data)
    
    return result


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    request: AdminUpdateUserRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Update user (admin only)"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can access this endpoint"
        )
    
    user = await User.filter(id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    await User.filter(id=user_id).update(
        email=request.email,
        full_name=request.full_name,
        is_superuser=request.is_superuser,
        is_active=request.is_active
    )
    
    updated_user = await User.get(id=user_id)
    return UserResponse.from_orm(updated_user)


@router.post("/admin/change-password")
async def admin_change_password(
    request: AdminChangePasswordRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Change another user's password (admin only)"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can access this endpoint"
        )
    
    user = await User.filter(id=request.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update password
    hashed_password = User.get_password_hash(request.new_password)
    await User.filter(id=request.user_id).update(hashed_password=hashed_password)
    
    return {"message": "Password changed successfully"}


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """Delete user (admin only)"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can access this endpoint"
        )
    
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    user = await User.filter(id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    await User.filter(id=user_id).delete()
    return {"message": "User deleted successfully"}


@router.post("/admin/set-subscription")
async def admin_set_subscription(
    request: AdminSetSubscriptionRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Set user subscription (admin only)"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can access this endpoint"
        )
    
    user = await User.filter(id=request.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    plan = await SubscriptionPlan.filter(id=request.plan_id).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found"
        )
    
    # Cancel existing active subscriptions
    await UserSubscription.filter(
        user=user,
        status="active"
    ).update(status="cancelled", cancelled_at=datetime.utcnow())
    
    # Create new subscription
    new_subscription = await UserSubscription.create(
        user=user,
        plan=plan,
        status="active",
        starts_at=datetime.utcnow(),
        ends_at=None  # Set based on plan billing period if needed
    )
    
    return {"message": f"User subscription set to {plan.name} successfully"}


@router.delete("/admin/cancel-subscription/{user_id}")
async def admin_cancel_subscription(
    user_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """Cancel user subscription (admin only)"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can access this endpoint"
        )
    
    user = await User.filter(id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Cancel active subscriptions
    updated = await UserSubscription.filter(
        user=user,
        status="active"
    ).update(status="cancelled", cancelled_at=datetime.utcnow())
    
    if updated == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active subscription found"
        )
    
    return {"message": "User subscription cancelled successfully"}


@router.post("/admin/create-user", response_model=UserResponse)
async def admin_create_user(
    request: AdminCreateUserRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Create new user (admin only)"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can access this endpoint"
        )
    
    # Check if user already exists
    existing_user = await User.filter(email=request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = await User.create(
        email=request.email,
        full_name=request.full_name,
        hashed_password=User.get_password_hash(request.password),
        language=request.language,
        is_superuser=request.is_superuser
    )
    
    # Send welcome email
    try:
        await email_service.send_welcome_email(user.email, user.full_name)
    except Exception as e:
        logger.warning(f"Failed to send welcome email: {e}")
    
    return UserResponse.from_orm(user)