"""
Users API Endpoints

Layer 6: HTTP Interface - User management endpoints.
Thin layer that validates DTOs and calls domain services.
"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.deps import UOWDep
from app.api.schemas.user import (
    UserCreate,
    UserRead,
    UserUpdate,
    UserResponse,
    UserListResponse,
    UserDeleteResponse,
)
from app.domain.entities.user import User as DomainUser
from app.core.logging.correlation import get_correlation_id

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user account with email and username validation."
)
async def create_user(
    user_data: UserCreate,
    uow: UOWDep
) -> UserResponse:
    """
    Layer 6: Create a new user.

    HTTP endpoint that validates input and calls domain logic.
    No business logic here - only DTO validation and domain service calls.
    """
    async with uow:
        # Check if user already exists
        existing_user = await uow.users.get_by_email(str(user_data.email))
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        existing_username = await uow.users.get_by_username(user_data.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username already exists"
            )

        # Create domain entity (business logic will be in domain service)
        # For now, creating directly - in full implementation, use UserService
        domain_user = DomainUser(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            password_hash=f"hashed_{user_data.password}",  # TODO: Proper hashing
            timezone=user_data.timezone,
            language=user_data.language,
        )

        # Create user
        created_user = await uow.users.create(domain_user)
        await uow.commit()

    return UserResponse(
        success=True,
        message="User created successfully",
        data=UserRead.model_validate(created_user.model_dump())
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Retrieve a user by their unique identifier."
)
async def get_user(
    user_id: UUID,
    uow: UOWDep
) -> UserResponse:
    """
    Layer 6: Get user by ID.

    Simple retrieval endpoint with error handling.
    """
    async with uow:
        user = await uow.users.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

    return UserResponse(
        success=True,
        message="User retrieved successfully",
        data=UserRead.model_validate(user.model_dump())
    )


@router.get(
    "",
    response_model=UserListResponse,
    summary="List all users",
    description="Retrieve a list of all users with optional filtering."
)
async def list_users(
    limit: int = 100,
    active_only: bool = False,
    uow: UOWDep
) -> UserListResponse:
    """
    Layer 6: List users with optional filtering.

    Supports pagination and filtering by active status.
    """
    async with uow:
        if active_only:
            users = await uow.users.find_active_users(limit=limit)
            total = await uow.users.count_users(active_only=True)
        else:
            # For now, use find_active_users for all users
            # In full implementation, add find_all method
            users = await uow.users.find_active_users(limit=limit)
            total = await uow.users.count_users()

    user_reads = [UserRead.model_validate(user.model_dump()) for user in users]

    return UserListResponse(
        success=True,
        message="Users retrieved successfully",
        data=user_reads,
        total=total
    )


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user",
    description="Update an existing user's information."
)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    uow: UOWDep
) -> UserResponse:
    """
    Layer 6: Update user information.

    Updates only provided fields, validates existence.
    """
    async with uow:
        # Get existing user
        user = await uow.users.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Update only provided fields
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(user, field):
                setattr(user, field, value)

        # Mark as updated and save
        user.mark_updated()
        await uow.users.update(user)
        await uow.commit()

        # Get updated user
        updated_user = await uow.users.get(user_id)

    return UserResponse(
        success=True,
        message="User updated successfully",
        data=UserRead.model_validate(updated_user.model_dump())
    )


@router.delete(
    "/{user_id}",
    response_model=UserDeleteResponse,
    summary="Delete user",
    description="Delete a user account permanently."
)
async def delete_user(
    user_id: UUID,
    uow: UOWDep
) -> UserDeleteResponse:
    """
    Layer 6: Delete user account.

    Permanently removes user from the system.
    """
    async with uow:
        # Check if user exists
        user = await uow.users.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Delete user
        deleted = await uow.users.delete(user_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete user"
            )

        await uow.commit()

    return UserDeleteResponse(
        success=True,
        message="User deleted successfully",
        user_id=user_id
    )


@router.get(
    "/email/{email}",
    response_model=UserResponse,
    summary="Get user by email",
    description="Retrieve a user by their email address."
)
async def get_user_by_email(
    email: str,
    uow: UOWDep
) -> UserResponse:
    """
    Layer 6: Get user by email.

    Convenience endpoint for email-based lookups.
    """
    async with uow:
        user = await uow.users.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

    return UserResponse(
        success=True,
        message="User retrieved successfully",
        data=UserRead.model_validate(user.model_dump())
    )


@router.get(
    "/username/{username}",
    response_model=UserResponse,
    summary="Get user by username",
    description="Retrieve a user by their username."
)
async def get_user_by_username(
    username: str,
    uow: UOWDep
) -> UserResponse:
    """
    Layer 6: Get user by username.

    Convenience endpoint for username-based lookups.
    """
    async with uow:
        user = await uow.users.get_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

    return UserResponse(
        success=True,
        message="User retrieved successfully",
        data=UserRead.model_validate(user.model_dump())
    )


@router.get(
    "/stats",
    summary="Get user statistics",
    description="Retrieve user statistics and counts."
)
async def get_user_stats(
    uow: UOWDep
) -> dict:
    """
    Layer 6: Get user statistics.

    Administrative endpoint for user metrics.
    """
    async with uow:
        total_users = await uow.users.count_users()
        active_users = await uow.users.count_users(active_only=True)

    return {
        "success": True,
        "message": "User statistics retrieved successfully",
        "data": {
            "total_users": total_users,
            "active_users": active_users,
            "inactive_users": total_users - active_users,
        }
    }