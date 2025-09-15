"""
User management endpoints.

Provides user profile management, user listing for admins,
and user-related operations.
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, EmailStr, Field

from app.api.deps.auth import get_current_user, require_permissions, CurrentUser
from app.api.deps.pagination import PaginationParams, PaginatedResponse
from app.core import get_logger

logger = get_logger(__name__)
router = APIRouter()


# Request/Response Models
class UserUpdateRequest(BaseModel):
    """User profile update request model."""
    full_name: Optional[str] = Field(None, min_length=2, max_length=100, description="Full name", example="John Doe")
    bio: Optional[str] = Field(None, max_length=500, description="User bio", example="Software developer")


class UserResponse(BaseModel):
    """User profile response model."""
    id: int = Field(description="User ID", example=1)
    email: str = Field(description="User email", example="user@example.com")
    full_name: str = Field(description="User full name", example="John Doe")
    bio: Optional[str] = Field(None, description="User bio", example="Software developer")
    is_active: bool = Field(description="User status", example=True)
    is_verified: bool = Field(description="Email verification status", example=True)
    created_at: str = Field(description="Registration date (DD.MM.YYYY)", example="01.01.2024")
    last_login: Optional[str] = Field(None, description="Last login date (DD.MM.YYYY)", example="01.01.2024")


class PublicUserResponse(BaseModel):
    """Public user profile response model (limited info)."""
    id: int = Field(description="User ID", example=1)
    full_name: str = Field(description="User full name", example="John Doe")
    bio: Optional[str] = Field(None, description="User bio", example="Software developer")
    created_at: str = Field(description="Registration date (DD.MM.YYYY)", example="01.01.2024")


class PasswordChangeRequest(BaseModel):
    """Password change request model."""
    current_password: str = Field(description="Current password")
    new_password: str = Field(min_length=8, max_length=128, description="New password", example="NewSecurePassword123!")


@router.get("/me", response_model=UserResponse)
async def get_my_profile(
    current_user: CurrentUser = Depends(get_current_user),
    # db: Database = Depends(get_database)  # TODO: Add when database layer is implemented
) -> UserResponse:
    """
    Get current user's detailed profile.

    Returns full profile information for the authenticated user.
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
        return UserResponse(
            id=current_user.user_id,
            email="user@example.com",
            full_name="John Doe",
            bio="Software developer",
            is_active=True,
            is_verified=True,
            created_at="01.01.2024",
            last_login="15.01.2024"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Profile fetch failed: {str(e)}", extra={"user_id": current_user.user_id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch profile"
        )


@router.put("/me", response_model=UserResponse)
async def update_my_profile(
    request: UserUpdateRequest,
    current_user: CurrentUser = Depends(get_current_user),
    # db: Database = Depends(get_database)  # TODO: Add when database layer is implemented
) -> UserResponse:
    """
    Update current user's profile.

    Updates user profile information with provided data.
    """
    try:
        logger.info(f"Profile update", extra={"user_id": current_user.user_id})

        # TODO: Replace with actual database operations
        # update_data = {}
        # if request.full_name is not None:
        #     update_data["full_name"] = request.full_name
        # if request.bio is not None:
        #     update_data["bio"] = request.bio

        # if update_data:
        #     update_data["updated_at"] = datetime.utcnow()
        #     await db.users.update_one(
        #         {"_id": current_user.user_id},
        #         {"$set": update_data}
        #     )

        # Mock updated user data
        return UserResponse(
            id=current_user.user_id,
            email="user@example.com",
            full_name=request.full_name or "John Doe",
            bio=request.bio,
            is_active=True,
            is_verified=True,
            created_at="01.01.2024",
            last_login="15.01.2024"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Profile update failed: {str(e)}", extra={"user_id": current_user.user_id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )


@router.post("/me/change-password")
async def change_password(
    request: PasswordChangeRequest,
    current_user: CurrentUser = Depends(get_current_user),
    # db: Database = Depends(get_database)  # TODO: Add when database layer is implemented
) -> dict:
    """
    Change current user's password.

    Validates current password and updates to new password.
    """
    try:
        logger.info(f"Password change request", extra={"user_id": current_user.user_id})

        # TODO: Replace with actual database operations
        # user = await db.users.find_one({"_id": current_user.user_id})
        # if not user or not verify_password(request.current_password, user["password_hash"]):
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Current password is incorrect"
        #     )

        # Hash new password and update
        # new_password_hash = get_password_hash(request.new_password)
        # await db.users.update_one(
        #     {"_id": current_user.user_id},
        #     {"$set": {
        #         "password_hash": new_password_hash,
        #         "updated_at": datetime.utcnow()
        #     }}
        # )

        logger.info(f"Password changed successfully", extra={"user_id": current_user.user_id})
        return {"message": "Password changed successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password change failed: {str(e)}", extra={"user_id": current_user.user_id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password"
        )


@router.get("/{user_id}", response_model=PublicUserResponse)
async def get_user_profile(
    user_id: int,
    # db: Database = Depends(get_database)  # TODO: Add when database layer is implemented
) -> PublicUserResponse:
    """
    Get public user profile by ID.

    Returns limited public information about a user.
    """
    try:
        logger.info(f"Public profile request", extra={"requested_user_id": user_id})

        # TODO: Replace with actual database operations
        # user = await db.users.find_one({"_id": user_id, "is_active": True})
        # if not user:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail="User not found"
        #     )

        if user_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Mock public user data
        return PublicUserResponse(
            id=user_id,
            full_name="John Doe",
            bio="Software developer",
            created_at="01.01.2024"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Public profile fetch failed: {str(e)}", extra={"requested_user_id": user_id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch user profile"
        )


@router.get("/", response_model=PaginatedResponse[UserResponse])
async def list_users(
    pagination: PaginationParams = Depends(),
    search: Optional[str] = Query(None, description="Search users by name or email"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    current_user: CurrentUser = Depends(require_permissions(["admin", "user_management"])),
    # db: Database = Depends(get_database)  # TODO: Add when database layer is implemented
) -> PaginatedResponse[UserResponse]:
    """
    List users with filtering and pagination.

    Requires admin permissions. Supports search and filtering.
    """
    try:
        logger.info(f"Users list request", extra={
            "admin_user_id": current_user.user_id,
            "search": search,
            "is_active": is_active,
            "pagination": {"offset": pagination.offset, "limit": pagination.limit}
        })

        # TODO: Replace with actual database operations
        # Build filter query
        # filter_query = {}
        # if search:
        #     filter_query["$or"] = [
        #         {"full_name": {"$regex": search, "$options": "i"}},
        #         {"email": {"$regex": search, "$options": "i"}}
        #     ]
        # if is_active is not None:
        #     filter_query["is_active"] = is_active

        # Get total count and users
        # total_count = await db.users.count_documents(filter_query)
        # users_cursor = db.users.find(filter_query).skip(pagination.offset).limit(pagination.limit)
        # users = await users_cursor.to_list(length=pagination.limit)

        # Mock user data
        mock_users = [
            UserResponse(
                id=1,
                email="user1@example.com",
                full_name="John Doe",
                bio="Software developer",
                is_active=True,
                is_verified=True,
                created_at="01.01.2024",
                last_login="15.01.2024"
            ),
            UserResponse(
                id=2,
                email="user2@example.com",
                full_name="Jane Smith",
                bio="Designer",
                is_active=True,
                is_verified=False,
                created_at="02.01.2024",
                last_login="14.01.2024"
            )
        ]

        return PaginatedResponse(
            items=mock_users,
            total=2,
            offset=pagination.offset,
            limit=pagination.limit
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Users list failed: {str(e)}", extra={"admin_user_id": current_user.user_id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch users"
        )