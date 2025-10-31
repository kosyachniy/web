"""
User API Endpoint Tests

Comprehensive API tests covering ALL user endpoints, methods, data flows,
and edge cases as mandated by CLAUDE.md TDD workflow.
"""

from __future__ import annotations

import pytest
from uuid import uuid4, UUID
from fastapi.testclient import TestClient
from fastapi import status
from unittest.mock import AsyncMock, patch

from app.domain.entities.user import UserStatus, UserRole


class TestCreateUser:
    """Test POST /api/v1/users/ endpoint."""

    def test_create_user_success(self, test_client: TestClient, sample_user_data: dict):
        """Test successful user creation."""
        response = test_client.post("/api/v1/users/", json=sample_user_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()

        assert data["success"] is True
        assert data["message"] == "User created successfully"
        assert "data" in data

        user_data = data["data"]
        assert user_data["email"] == sample_user_data["email"]
        assert user_data["username"] == sample_user_data["username"]
        assert user_data["full_name"] == sample_user_data["full_name"]
        assert user_data["timezone"] == sample_user_data["timezone"]
        assert user_data["language"] == sample_user_data["language"]
        assert "password" not in user_data  # Password should never be returned
        assert "password_hash" not in user_data  # Hash should never be returned
        assert "id" in user_data
        assert "created_at" in user_data

    def test_create_user_duplicate_email(self, test_client: TestClient, sample_user_data: dict):
        """Test user creation with duplicate email fails."""
        # Create first user
        test_client.post("/api/v1/users/", json=sample_user_data)

        # Try to create second user with same email
        duplicate_data = sample_user_data.copy()
        duplicate_data["username"] = "differentuser"

        response = test_client.post("/api/v1/users/", json=duplicate_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = response.json()
        assert "User with this email already exists" in error["detail"]

    def test_create_user_duplicate_username(self, test_client: TestClient, sample_user_data: dict):
        """Test user creation with duplicate username fails."""
        # Create first user
        test_client.post("/api/v1/users/", json=sample_user_data)

        # Try to create second user with same username
        duplicate_data = sample_user_data.copy()
        duplicate_data["email"] = "different@example.com"

        response = test_client.post("/api/v1/users/", json=duplicate_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = response.json()
        assert "User with this username already exists" in error["detail"]

    @pytest.mark.parametrize("field,value,expected_error", [
        ("email", "", "validation_error"),
        ("email", "invalid-email", "validation_error"),
        ("email", "a" * 256, "validation_error"),  # Too long
        ("username", "", "validation_error"),
        ("username", "a", "validation_error"),  # Too short
        ("username", "a" * 51, "validation_error"),  # Too long
        ("username", "user@name", "validation_error"),  # Invalid chars
        ("password", "", "validation_error"),
        ("password", "123", "validation_error"),  # Too short
        ("full_name", "A" * 101, "validation_error"),  # Too long
        ("timezone", "Invalid/Zone", "validation_error"),
        ("language", "invalid", "validation_error"),
    ])
    def test_create_user_validation_errors(
        self, test_client: TestClient, sample_user_data: dict, field: str, value: str, expected_error: str
    ):
        """Test user creation validation for various invalid inputs."""
        invalid_data = sample_user_data.copy()
        invalid_data[field] = value

        response = test_client.post("/api/v1/users/", json=invalid_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        error = response.json()
        assert "detail" in error
        assert any(field in str(err.get("loc", [])) for err in error["detail"])

    def test_create_user_missing_required_fields(self, test_client: TestClient):
        """Test user creation with missing required fields."""
        incomplete_data = {"email": "test@example.com"}  # Missing required fields

        response = test_client.post("/api/v1/users/", json=incomplete_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        error = response.json()
        assert "detail" in error

    def test_create_user_empty_body(self, test_client: TestClient):
        """Test user creation with empty request body."""
        response = test_client.post("/api/v1/users/", json={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_user_invalid_json(self, test_client: TestClient):
        """Test user creation with invalid JSON."""
        response = test_client.post(
            "/api/v1/users/",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @patch('app.adapters.database.postgres.repositories.user_repo.PgUserRepo.create')
    def test_create_user_database_error(self, mock_create, test_client: TestClient, sample_user_data: dict):
        """Test user creation when database error occurs."""
        mock_create.side_effect = Exception("Database connection failed")

        response = test_client.post("/api/v1/users/", json=sample_user_data)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_create_user_boundary_values(self, test_client: TestClient, boundary_user_data: dict):
        """Test user creation with boundary values."""
        response = test_client.post("/api/v1/users/", json=boundary_user_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["success"] is True


class TestGetUser:
    """Test GET /api/v1/users/{user_id} endpoint."""

    def test_get_user_success(self, test_client: TestClient, sample_user_data: dict):
        """Test successful user retrieval."""
        # Create user first
        create_response = test_client.post("/api/v1/users/", json=sample_user_data)
        user_id = create_response.json()["data"]["id"]

        # Get user
        response = test_client.get(f"/api/v1/users/{user_id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["success"] is True
        assert data["message"] == "User retrieved successfully"
        assert data["data"]["id"] == user_id
        assert data["data"]["email"] == sample_user_data["email"]

    def test_get_user_not_found(self, test_client: TestClient):
        """Test getting non-existent user."""
        non_existent_id = str(uuid4())

        response = test_client.get(f"/api/v1/users/{non_existent_id}")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        error = response.json()
        assert "User not found" in error["detail"]

    def test_get_user_invalid_uuid(self, test_client: TestClient):
        """Test getting user with invalid UUID format."""
        invalid_id = "invalid-uuid-format"

        response = test_client.get(f"/api/v1/users/{invalid_id}")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @patch('app.adapters.database.postgres.repositories.user_repo.PgUserRepo.get')
    def test_get_user_database_error(self, mock_get, test_client: TestClient):
        """Test user retrieval when database error occurs."""
        mock_get.side_effect = Exception("Database connection failed")
        user_id = str(uuid4())

        response = test_client.get(f"/api/v1/users/{user_id}")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


class TestListUsers:
    """Test GET /api/v1/users/ endpoint."""

    def test_list_users_success(self, test_client: TestClient, multiple_users_data: list[dict]):
        """Test successful users listing."""
        # Create multiple users
        for user_data in multiple_users_data:
            test_client.post("/api/v1/users/", json=user_data)

        response = test_client.get("/api/v1/users/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["success"] is True
        assert data["message"] == "Users retrieved successfully"
        assert "data" in data
        assert "total" in data
        assert len(data["data"]) == len(multiple_users_data)

    def test_list_users_with_limit(self, test_client: TestClient, multiple_users_data: list[dict]):
        """Test users listing with limit parameter."""
        # Create multiple users
        for user_data in multiple_users_data:
            test_client.post("/api/v1/users/", json=user_data)

        limit = 3
        response = test_client.get(f"/api/v1/users/?limit={limit}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["data"]) <= limit

    def test_list_users_active_only(self, test_client: TestClient, multiple_users_data: list[dict]):
        """Test users listing with active_only filter."""
        # Create multiple users
        for user_data in multiple_users_data:
            test_client.post("/api/v1/users/", json=user_data)

        response = test_client.get("/api/v1/users/?active_only=true")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # All returned users should be active
        for user in data["data"]:
            assert user.get("status") == UserStatus.ACTIVE.value

    def test_list_users_empty_result(self, test_client: TestClient):
        """Test users listing when no users exist."""
        response = test_client.get("/api/v1/users/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["success"] is True
        assert data["data"] == []
        assert data["total"] == 0

    @pytest.mark.parametrize("limit", [-1, 0, 1001])  # Invalid limits
    def test_list_users_invalid_limit(self, test_client: TestClient, limit: int):
        """Test users listing with invalid limit values."""
        response = test_client.get(f"/api/v1/users/?limit={limit}")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @patch('app.adapters.database.postgres.repositories.user_repo.PgUserRepo.find_active_users')
    def test_list_users_database_error(self, mock_find, test_client: TestClient):
        """Test users listing when database error occurs."""
        mock_find.side_effect = Exception("Database connection failed")

        response = test_client.get("/api/v1/users/")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


class TestUpdateUser:
    """Test PUT /api/v1/users/{user_id} endpoint."""

    def test_update_user_success(self, test_client: TestClient, sample_user_data: dict):
        """Test successful user update."""
        # Create user first
        create_response = test_client.post("/api/v1/users/", json=sample_user_data)
        user_id = create_response.json()["data"]["id"]

        # Update user
        update_data = {
            "full_name": "Updated Name",
            "timezone": "Europe/London"
        }

        response = test_client.put(f"/api/v1/users/{user_id}", json=update_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["success"] is True
        assert data["message"] == "User updated successfully"
        assert data["data"]["full_name"] == update_data["full_name"]
        assert data["data"]["timezone"] == update_data["timezone"]
        # Original data should remain unchanged
        assert data["data"]["email"] == sample_user_data["email"]

    def test_update_user_not_found(self, test_client: TestClient):
        """Test updating non-existent user."""
        non_existent_id = str(uuid4())
        update_data = {"full_name": "Updated Name"}

        response = test_client.put(f"/api/v1/users/{non_existent_id}", json=update_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        error = response.json()
        assert "User not found" in error["detail"]

    def test_update_user_partial_update(self, test_client: TestClient, sample_user_data: dict):
        """Test partial user update."""
        # Create user first
        create_response = test_client.post("/api/v1/users/", json=sample_user_data)
        user_id = create_response.json()["data"]["id"]

        # Update only one field
        update_data = {"language": "es"}

        response = test_client.put(f"/api/v1/users/{user_id}", json=update_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["data"]["language"] == "es"
        # Other fields should remain unchanged
        assert data["data"]["email"] == sample_user_data["email"]
        assert data["data"]["full_name"] == sample_user_data["full_name"]

    def test_update_user_empty_update(self, test_client: TestClient, sample_user_data: dict):
        """Test user update with empty data."""
        # Create user first
        create_response = test_client.post("/api/v1/users/", json=sample_user_data)
        user_id = create_response.json()["data"]["id"]

        response = test_client.put(f"/api/v1/users/{user_id}", json={})

        assert response.status_code == status.HTTP_200_OK  # Should succeed with no changes

    def test_update_user_invalid_uuid(self, test_client: TestClient):
        """Test updating user with invalid UUID format."""
        invalid_id = "invalid-uuid-format"
        update_data = {"full_name": "Updated Name"}

        response = test_client.put(f"/api/v1/users/{invalid_id}", json=update_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestDeleteUser:
    """Test DELETE /api/v1/users/{user_id} endpoint."""

    def test_delete_user_success(self, test_client: TestClient, sample_user_data: dict):
        """Test successful user deletion."""
        # Create user first
        create_response = test_client.post("/api/v1/users/", json=sample_user_data)
        user_id = create_response.json()["data"]["id"]

        # Delete user
        response = test_client.delete(f"/api/v1/users/{user_id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["success"] is True
        assert data["message"] == "User deleted successfully"
        assert data["user_id"] == user_id

        # Verify user is deleted
        get_response = test_client.get(f"/api/v1/users/{user_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_user_not_found(self, test_client: TestClient):
        """Test deleting non-existent user."""
        non_existent_id = str(uuid4())

        response = test_client.delete(f"/api/v1/users/{non_existent_id}")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        error = response.json()
        assert "User not found" in error["detail"]

    def test_delete_user_invalid_uuid(self, test_client: TestClient):
        """Test deleting user with invalid UUID format."""
        invalid_id = "invalid-uuid-format"

        response = test_client.delete(f"/api/v1/users/{invalid_id}")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetUserByEmail:
    """Test GET /api/v1/users/email/{email} endpoint."""

    def test_get_user_by_email_success(self, test_client: TestClient, sample_user_data: dict):
        """Test successful user retrieval by email."""
        # Create user first
        test_client.post("/api/v1/users/", json=sample_user_data)

        # Get user by email
        response = test_client.get(f"/api/v1/users/email/{sample_user_data['email']}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["success"] is True
        assert data["data"]["email"] == sample_user_data["email"]

    def test_get_user_by_email_not_found(self, test_client: TestClient):
        """Test getting user by non-existent email."""
        non_existent_email = "nonexistent@example.com"

        response = test_client.get(f"/api/v1/users/email/{non_existent_email}")

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestGetUserByUsername:
    """Test GET /api/v1/users/username/{username} endpoint."""

    def test_get_user_by_username_success(self, test_client: TestClient, sample_user_data: dict):
        """Test successful user retrieval by username."""
        # Create user first
        test_client.post("/api/v1/users/", json=sample_user_data)

        # Get user by username
        response = test_client.get(f"/api/v1/users/username/{sample_user_data['username']}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["success"] is True
        assert data["data"]["username"] == sample_user_data["username"]

    def test_get_user_by_username_not_found(self, test_client: TestClient):
        """Test getting user by non-existent username."""
        non_existent_username = "nonexistentuser"

        response = test_client.get(f"/api/v1/users/username/{non_existent_username}")

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestGetUserStats:
    """Test GET /api/v1/users/stats endpoint."""

    def test_get_user_stats_success(self, test_client: TestClient, multiple_users_data: list[dict]):
        """Test successful user statistics retrieval."""
        # Create multiple users
        for user_data in multiple_users_data:
            test_client.post("/api/v1/users/", json=user_data)

        response = test_client.get("/api/v1/users/stats")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["success"] is True
        assert data["message"] == "User statistics retrieved successfully"
        assert "data" in data

        stats = data["data"]
        assert "total_users" in stats
        assert "active_users" in stats
        assert "inactive_users" in stats
        assert stats["total_users"] == len(multiple_users_data)

    def test_get_user_stats_empty(self, test_client: TestClient):
        """Test user statistics when no users exist."""
        response = test_client.get("/api/v1/users/stats")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        stats = data["data"]
        assert stats["total_users"] == 0
        assert stats["active_users"] == 0
        assert stats["inactive_users"] == 0


class TestErrorHandling:
    """Test global error handling and edge cases."""

    def test_method_not_allowed(self, test_client: TestClient):
        """Test unsupported HTTP methods."""
        response = test_client.patch("/api/v1/users/")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_content_type_validation(self, test_client: TestClient, sample_user_data: dict):
        """Test request with wrong content type."""
        response = test_client.post(
            "/api/v1/users/",
            data="not json",
            headers={"Content-Type": "text/plain"}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_large_payload(self, test_client: TestClient):
        """Test request with very large payload."""
        large_data = {
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "A" * 10000,  # Very large name
            "password": "SecurePass123!"
        }

        response = test_client.post("/api/v1/users/", json=large_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_concurrent_requests(self, test_client: TestClient, multiple_users_data: list[dict]):
        """Test handling of concurrent requests."""
        import asyncio
        import httpx

        async def create_user(client, user_data):
            response = client.post("/api/v1/users/", json=user_data)
            return response

        # Create concurrent requests
        tasks = []
        async with httpx.AsyncClient(app=test_client.app, base_url="http://test") as client:
            for user_data in multiple_users_data:
                tasks.append(create_user(client, user_data))

            responses = await asyncio.gather(*tasks)

        # All requests should succeed
        for response in responses:
            assert response.status_code == status.HTTP_201_CREATED