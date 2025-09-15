"""
Authentication and authorization endpoints.

Provides JWT-based authentication with access and refresh token support,
user registration, login, logout, and token management.
"""
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel, EmailStr, Field

from app.api.deps.auth import get_current_user, CurrentUser
from app.core import settings, get_logger
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token
)

logger = get_logger(__name__)
router = APIRouter()
security = HTTPBearer()


# Request/Response Models
class UserRegistrationRequest(BaseModel):
    """User registration request model."""
    email: EmailStr = Field(description="User email address", example="user@example.com")
    password: str = Field(min_length=8, max_length=128, description="User password", example="SecurePassword123!")
    full_name: str = Field(min_length=2, max_length=100, description="Full name", example="John Doe")


class LoginRequest(BaseModel):
    """User login request model."""
    email: EmailStr = Field(description="User email address", example="user@example.com")
    password: str = Field(description="User password", example="SecurePassword123!")


class TokenResponse(BaseModel):
    """Token response model."""
    access_token: str = Field(description="JWT access token")
    refresh_token: str = Field(description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(description="Access token expiration time in seconds")


class RefreshTokenRequest(BaseModel):
    """Refresh token request model."""
    refresh_token: str = Field(description="Valid refresh token")


class UserProfileResponse(BaseModel):
    """User profile response model."""
    id: int = Field(description="User ID", example=1)
    email: str = Field(description="User email", example="user@example.com")
    full_name: str = Field(description="User full name", example="John Doe")
    is_active: bool = Field(description="User status", example=True)
    created_at: str = Field(description="Registration date (DD.MM.YYYY)", example="01.01.2024")


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: UserRegistrationRequest,
    # db: Database = Depends(get_database)  # TODO: Add when database layer is implemented
) -> TokenResponse:
    """
    Register a new user account.

    Creates a new user with hashed password and returns authentication tokens.
    """
    try:
        logger.info(f"User registration attempt", extra={"email": request.email})

        # TODO: Replace with actual database operations
        # Check if user already exists
        # existing_user = await db.users.find_one({"email": request.email})
        # if existing_user:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="User with this email already exists"
        #     )

        # Hash password and create user
        password_hash = get_password_hash(request.password)

        # TODO: Create user in database
        # user_data = {
        #     "email": request.email,
        #     "password_hash": password_hash,
        #     "full_name": request.full_name,
        #     "is_active": True,
        #     "created_at": datetime.utcnow()
        # }
        # result = await db.users.insert_one(user_data)
        # user_id = result.inserted_id

        # Mock user ID for now
        user_id = 1

        # Generate tokens
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(subject=user_id, expires_delta=access_token_expires)
        refresh_token = create_refresh_token(subject=user_id)

        logger.info(f"User registered successfully", extra={"user_id": user_id})

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.access_token_expire_minutes * 60
        )

    except Exception as e:
        logger.error(f"Registration failed: {str(e)}", extra={"email": request.email})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    # db: Database = Depends(get_database)  # TODO: Add when database layer is implemented
) -> TokenResponse:
    """
    Authenticate user and return tokens.

    Validates credentials and returns JWT access and refresh tokens.
    """
    try:
        logger.info(f"Login attempt", extra={"email": request.email})

        # TODO: Replace with actual database operations
        # user = await db.users.find_one({"email": request.email})
        # if not user or not verify_password(request.password, user["password_hash"]):
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="Invalid email or password"
        #     )

        # Mock password verification for now
        if request.password != "SecurePassword123!":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Mock user data
        user_id = 1

        # Generate tokens
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(subject=user_id, expires_delta=access_token_expires)
        refresh_token = create_refresh_token(subject=user_id)

        logger.info(f"User logged in successfully", extra={"user_id": user_id})

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.access_token_expire_minutes * 60
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login failed: {str(e)}", extra={"email": request.email})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_access_token(request: RefreshTokenRequest) -> TokenResponse:
    """
    Refresh access token using valid refresh token.

    Validates refresh token and returns new access token.
    """
    try:
        # Decode and validate refresh token
        token_payload = decode_token(request.refresh_token, token_type="refresh")
        user_id = token_payload["sub"]

        logger.info(f"Token refresh", extra={"user_id": user_id})

        # TODO: Validate user still exists and is active
        # user = await db.users.find_one({"_id": user_id, "is_active": True})
        # if not user:
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="User not found or inactive"
        #     )

        # Generate new access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(subject=user_id, expires_delta=access_token_expires)

        return TokenResponse(
            access_token=access_token,
            refresh_token=request.refresh_token,  # Keep the same refresh token
            expires_in=settings.access_token_expire_minutes * 60
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.post("/logout")
async def logout(current_user: CurrentUser = Depends(get_current_user)) -> dict[str, Any]:
    """
    Logout user and invalidate tokens.

    Adds tokens to blacklist to prevent further use.
    """
    try:
        logger.info(f"User logout", extra={"user_id": current_user.user_id})

        # TODO: Add token to blacklist in Redis
        # token_jti = current_user.token_payload.get("jti")
        # if token_jti:
        #     await redis_client.setex(
        #         f"blacklist:{token_jti}",
        #         settings.access_token_expire_minutes * 60,
        #         "true"
        #     )

        return {"message": "Successfully logged out"}

    except Exception as e:
        logger.error(f"Logout failed: {str(e)}", extra={"user_id": current_user.user_id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )


@router.get("/me", response_model=UserProfileResponse)
async def get_current_user_profile(
    current_user: CurrentUser = Depends(get_current_user),
    # db: Database = Depends(get_database)  # TODO: Add when database layer is implemented
) -> UserProfileResponse:
    """
    Get current user profile information.

    Returns authenticated user's profile data.
    """
    try:
        logger.info(f"Profile request", extra={"user_id": current_user.user_id})

        # TODO: Replace with actual database operations
        # user = await db.users.find_one({"_id": current_user.user_id})
        # if not user:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail="User not found"
        #     )

        # Mock user data
        return UserProfileResponse(
            id=current_user.user_id,
            email="user@example.com",
            full_name="John Doe",
            is_active=True,
            created_at="01.01.2024"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Profile fetch failed: {str(e)}", extra={"user_id": current_user.user_id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch profile"
        )