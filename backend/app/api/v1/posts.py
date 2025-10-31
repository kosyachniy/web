"""
Posts API Endpoints

Layer 6: HTTP Interface - Posts management endpoints.
Minimal implementation to get frontend working.
"""

from __future__ import annotations

from typing import Optional, Union

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/posts", tags=["Posts"])


# Request/Response schemas
class PostAuthor(BaseModel):
    """Post author data."""
    id: int
    login: str
    name: Optional[str] = None
    surname: Optional[str] = None
    title: Optional[str] = None
    image: Optional[str] = None


class PostCategoryData(BaseModel):
    """Post category data."""
    id: int
    url: str
    title: str
    parents: list[dict] = Field(default_factory=list)


class Post(BaseModel):
    """Post model."""
    id: int
    title: str
    description: Optional[str] = None
    data: str  # Content
    image: Optional[str] = None
    url: str
    created: int  # Unix timestamp
    updated: int  # Unix timestamp
    status: int = 1
    category: Optional[int] = None
    locale: str = "en"
    user: Optional[int] = None
    views: int = 0

    # Extended fields
    category_data: Optional[PostCategoryData] = None
    author: Optional[PostAuthor] = None


class PostsGetRequest(BaseModel):
    """Request model for getting posts."""
    id: Optional[Union[int, list[int]]] = None
    limit: int = Field(default=12, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
    search: Optional[str] = None
    my: bool = False
    category: Optional[int] = None
    locale: Optional[str] = None
    utm: Optional[str] = None


class PostsGetResponse(BaseModel):
    """Response model for posts list."""
    posts: list[Post]
    count: int


# Mock data for development
MOCK_POSTS: list[dict] = [
    {
        "id": 1,
        "title": "Welcome to Our Platform",
        "description": "Getting started guide for new users",
        "data": "This is a comprehensive guide to help you get started...",
        "image": None,
        "url": "welcome-to-our-platform",
        "created": 1704067200,
        "updated": 1704067200,
        "status": 1,
        "category": 1,
        "locale": "en",
        "user": 1,
        "views": 150
    },
    {
        "id": 2,
        "title": "Technology Trends 2024",
        "description": "Exploring the latest trends in technology",
        "data": "The technology landscape is evolving rapidly...",
        "image": None,
        "url": "technology-trends-2024",
        "created": 1704153600,
        "updated": 1704153600,
        "status": 1,
        "category": 1,
        "locale": "en",
        "user": 1,
        "views": 320
    },
    {
        "id": 3,
        "title": "Business Strategy Guide",
        "description": "Essential strategies for business growth",
        "data": "Learn the key strategies to grow your business...",
        "image": None,
        "url": "business-strategy-guide",
        "created": 1704240000,
        "updated": 1704240000,
        "status": 1,
        "category": 2,
        "locale": "en",
        "user": 1,
        "views": 200
    }
]


@router.post(
    "/get/",
    response_model=PostsGetResponse,
    summary="Get posts",
    description="Get list of posts with optional filtering and pagination."
)
async def get_posts(request: PostsGetRequest) -> PostsGetResponse:
    """
    Get posts with optional filtering.

    Currently returns mock data for development.
    TODO: Implement real database queries once migrations are applied.
    """
    # Filter mock data based on request parameters
    filtered_posts = MOCK_POSTS.copy()

    # Filter by ID(s)
    if request.id is not None:
        if isinstance(request.id, int):
            filtered_posts = [post for post in filtered_posts if post["id"] == request.id]
        else:  # list of IDs
            filtered_posts = [post for post in filtered_posts if post["id"] in request.id]

    # Filter by category
    if request.category is not None:
        filtered_posts = [post for post in filtered_posts if post.get("category") == request.category]

    # Filter by locale
    if request.locale is not None:
        filtered_posts = [post for post in filtered_posts if post.get("locale") == request.locale]

    # Search filter
    if request.search:
        search_lower = request.search.lower()
        filtered_posts = [
            post for post in filtered_posts
            if search_lower in post.get("title", "").lower()
            or search_lower in post.get("description", "").lower()
            or search_lower in post.get("data", "").lower()
        ]

    # Total count before pagination
    total_count = len(filtered_posts)

    # Apply pagination
    start = request.offset
    end = request.offset + request.limit
    paginated_posts = filtered_posts[start:end]

    # Convert to Post models
    posts = [Post(**post) for post in paginated_posts]

    return PostsGetResponse(
        posts=posts,
        count=total_count
    )


@router.get(
    "/{post_id}/",
    response_model=Post,
    summary="Get post by ID",
    description="Get a single post by its ID."
)
async def get_post(post_id: int) -> Post:
    """
    Get a post by ID.

    Currently returns mock data for development.
    TODO: Implement real database queries once migrations are applied.
    """
    # Find post in mock data
    post_data = next((post for post in MOCK_POSTS if post["id"] == post_id), None)

    if not post_data:
        # Return a default post
        post_data = {
            "id": post_id,
            "title": f"Post {post_id}",
            "description": "Post description",
            "data": "Post content goes here...",
            "image": None,
            "url": f"post-{post_id}",
            "created": 1704067200,
            "updated": 1704067200,
            "status": 1,
            "category": 1,
            "locale": "en",
            "user": 1,
            "views": 0
        }

    return Post(**post_data)


@router.post(
    "/",
    response_model=Post,
    status_code=201,
    summary="Create post",
    description="Create a new post."
)
async def create_post(post_data: dict) -> Post:
    """
    Create a new post.

    Currently returns mock data for development.
    TODO: Implement real database queries once migrations are applied.
    """
    # Mock implementation - just return a new post
    new_post = {
        "id": len(MOCK_POSTS) + 1,
        "title": post_data.get("title", "New Post"),
        "description": post_data.get("description"),
        "data": post_data.get("data", ""),
        "image": post_data.get("image"),
        "url": post_data.get("url", "new-post"),
        "created": 1704067200,
        "updated": 1704067200,
        "status": 1,
        "category": post_data.get("category"),
        "locale": post_data.get("locale", "en"),
        "user": post_data.get("user", 1),
        "views": 0
    }

    return Post(**new_post)


@router.put(
    "/{post_id}/",
    response_model=Post,
    summary="Update post",
    description="Update an existing post."
)
async def update_post(post_id: int, post_data: dict) -> Post:
    """
    Update a post.

    Currently returns mock data for development.
    TODO: Implement real database queries once migrations are applied.
    """
    # Find post and update
    post = next((post for post in MOCK_POSTS if post["id"] == post_id), None)

    if post:
        post.update(post_data)
        return Post(**post)

    # If not found, return the data as is
    return Post(id=post_id, **post_data)


@router.delete(
    "/{post_id}/",
    status_code=204,
    summary="Delete post",
    description="Delete a post."
)
async def delete_post(post_id: int):
    """
    Delete a post.

    Currently mock implementation.
    TODO: Implement real database queries once migrations are applied.
    """
    # Mock implementation - just return success
    return None
