"""
Posts management endpoints.

Provides CRUD operations for posts, including creation, reading,
updating, deletion, and advanced filtering/searching.
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.api.deps.auth import get_current_user, get_optional_user, CurrentUser
from app.api.deps.pagination import PaginationParams, PaginatedResponse
from app.core import get_logger

logger = get_logger(__name__)
router = APIRouter()


# Request/Response Models
class PostCreateRequest(BaseModel):
    """Post creation request model."""
    title: str = Field(min_length=1, max_length=200, description="Post title", example="My Awesome Post")
    content: str = Field(min_length=1, description="Post content in markdown", example="This is the post content...")
    category_id: Optional[int] = Field(None, gt=0, description="Category ID", example=1)
    tags: Optional[List[str]] = Field(None, max_items=10, description="Post tags", example=["tech", "programming"])
    is_published: bool = Field(default=True, description="Publication status", example=True)


class PostUpdateRequest(BaseModel):
    """Post update request model."""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Post title", example="Updated Post Title")
    content: Optional[str] = Field(None, min_length=1, description="Post content in markdown", example="Updated content...")
    category_id: Optional[int] = Field(None, gt=0, description="Category ID", example=1)
    tags: Optional[List[str]] = Field(None, max_items=10, description="Post tags", example=["tech", "programming"])
    is_published: Optional[bool] = Field(None, description="Publication status", example=True)


class CategoryResponse(BaseModel):
    """Category response model."""
    id: int = Field(description="Category ID", example=1)
    name: str = Field(description="Category name", example="Technology")
    slug: str = Field(description="Category slug", example="technology")


class AuthorResponse(BaseModel):
    """Post author response model."""
    id: int = Field(description="User ID", example=1)
    full_name: str = Field(description="Author name", example="John Doe")


class PostResponse(BaseModel):
    """Post response model."""
    id: int = Field(description="Post ID", example=1)
    title: str = Field(description="Post title", example="My Awesome Post")
    content: str = Field(description="Post content", example="This is the post content...")
    category: Optional[CategoryResponse] = Field(None, description="Post category")
    author: AuthorResponse = Field(description="Post author")
    tags: List[str] = Field(default=[], description="Post tags", example=["tech", "programming"])
    views_count: int = Field(default=0, description="Number of views", example=42)
    likes_count: int = Field(default=0, description="Number of likes", example=5)
    comments_count: int = Field(default=0, description="Number of comments", example=3)
    is_published: bool = Field(description="Publication status", example=True)
    is_liked_by_user: Optional[bool] = Field(None, description="Whether current user liked this post")
    created_at: str = Field(description="Creation date (DD.MM.YYYY)", example="01.01.2024")
    updated_at: Optional[str] = Field(None, description="Last update date (DD.MM.YYYY)", example="15.01.2024")


class PostSummaryResponse(BaseModel):
    """Post summary response model (for lists)."""
    id: int = Field(description="Post ID", example=1)
    title: str = Field(description="Post title", example="My Awesome Post")
    excerpt: str = Field(description="Post excerpt", example="This is a brief excerpt...")
    category: Optional[CategoryResponse] = Field(None, description="Post category")
    author: AuthorResponse = Field(description="Post author")
    tags: List[str] = Field(default=[], description="Post tags", example=["tech", "programming"])
    views_count: int = Field(default=0, description="Number of views", example=42)
    likes_count: int = Field(default=0, description="Number of likes", example=5)
    comments_count: int = Field(default=0, description="Number of comments", example=3)
    is_published: bool = Field(description="Publication status", example=True)
    is_liked_by_user: Optional[bool] = Field(None, description="Whether current user liked this post")
    created_at: str = Field(description="Creation date (DD.MM.YYYY)", example="01.01.2024")


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    request: PostCreateRequest,
    current_user: CurrentUser = Depends(get_current_user),
    # db: Database = Depends(get_database)  # TODO: Add when database layer is implemented
) -> PostResponse:
    """
    Create a new post.

    Creates a new post with the provided content and metadata.
    """
    try:
        logger.info(f"Creating post", extra={
            "user_id": current_user.user_id,
            "title": request.title,
            "category_id": request.category_id
        })

        # TODO: Replace with actual database operations
        # Validate category if provided
        # if request.category_id:
        #     category = await db.categories.find_one({"_id": request.category_id})
        #     if not category:
        #         raise HTTPException(
        #             status_code=status.HTTP_400_BAD_REQUEST,
        #             detail="Category not found"
        #         )

        # Create post document
        # post_data = {
        #     "title": request.title,
        #     "content": request.content,
        #     "author_id": current_user.user_id,
        #     "category_id": request.category_id,
        #     "tags": request.tags or [],
        #     "is_published": request.is_published,
        #     "views_count": 0,
        #     "likes_count": 0,
        #     "comments_count": 0,
        #     "created_at": datetime.utcnow(),
        #     "updated_at": datetime.utcnow()
        # }

        # result = await db.posts.insert_one(post_data)
        # post_id = result.inserted_id

        # Mock post data
        post_id = 1

        logger.info(f"Post created successfully", extra={
            "post_id": post_id,
            "user_id": current_user.user_id
        })

        return PostResponse(
            id=post_id,
            title=request.title,
            content=request.content,
            category=CategoryResponse(id=1, name="Technology", slug="technology") if request.category_id else None,
            author=AuthorResponse(id=current_user.user_id, full_name="John Doe"),
            tags=request.tags or [],
            views_count=0,
            likes_count=0,
            comments_count=0,
            is_published=request.is_published,
            is_liked_by_user=False,
            created_at="15.01.2024"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Post creation failed: {str(e)}", extra={"user_id": current_user.user_id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create post"
        )


@router.get("/", response_model=PaginatedResponse[PostSummaryResponse])
async def list_posts(
    pagination: PaginationParams = Depends(),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    search: Optional[str] = Query(None, description="Search in title and content"),
    author_id: Optional[int] = Query(None, description="Filter by author ID"),
    is_published: Optional[bool] = Query(True, description="Filter by publication status"),
    sort_by: str = Query("created_at", description="Sort field", regex="^(created_at|updated_at|views_count|likes_count)$"),
    sort_order: str = Query("desc", description="Sort order", regex="^(asc|desc)$"),
    current_user: Optional[CurrentUser] = Depends(get_optional_user),
    # db: Database = Depends(get_database)  # TODO: Add when database layer is implemented
) -> PaginatedResponse[PostSummaryResponse]:
    """
    List posts with filtering and pagination.

    Supports filtering by category, tags, author, and search queries.
    """
    try:
        logger.info(f"Posts list request", extra={
            "user_id": current_user.user_id if current_user else None,
            "category_id": category_id,
            "tag": tag,
            "search": search,
            "author_id": author_id,
            "pagination": {"offset": pagination.offset, "limit": pagination.limit}
        })

        # TODO: Replace with actual database operations
        # Build filter query
        # filter_query = {}
        # if is_published is not None:
        #     filter_query["is_published"] = is_published
        # if category_id:
        #     filter_query["category_id"] = category_id
        # if tag:
        #     filter_query["tags"] = {"$in": [tag]}
        # if author_id:
        #     filter_query["author_id"] = author_id
        # if search:
        #     filter_query["$or"] = [
        #         {"title": {"$regex": search, "$options": "i"}},
        #         {"content": {"$regex": search, "$options": "i"}}
        #     ]

        # Build sort criteria
        # sort_direction = 1 if sort_order == "asc" else -1
        # sort_criteria = [(sort_by, sort_direction)]

        # Get total count and posts
        # total_count = await db.posts.count_documents(filter_query)
        # posts_cursor = db.posts.find(filter_query).sort(sort_criteria).skip(pagination.offset).limit(pagination.limit)
        # posts = await posts_cursor.to_list(length=pagination.limit)

        # Mock posts data
        mock_posts = [
            PostSummaryResponse(
                id=1,
                title="My Awesome Post",
                excerpt="This is a brief excerpt of the post content...",
                category=CategoryResponse(id=1, name="Technology", slug="technology"),
                author=AuthorResponse(id=1, full_name="John Doe"),
                tags=["tech", "programming"],
                views_count=42,
                likes_count=5,
                comments_count=3,
                is_published=True,
                is_liked_by_user=False if current_user else None,
                created_at="01.01.2024"
            ),
            PostSummaryResponse(
                id=2,
                title="Another Great Post",
                excerpt="Another interesting post excerpt...",
                category=CategoryResponse(id=2, name="Design", slug="design"),
                author=AuthorResponse(id=2, full_name="Jane Smith"),
                tags=["design", "ui"],
                views_count=28,
                likes_count=8,
                comments_count=2,
                is_published=True,
                is_liked_by_user=True if current_user else None,
                created_at="02.01.2024"
            )
        ]

        return PaginatedResponse(
            items=mock_posts,
            total=2,
            offset=pagination.offset,
            limit=pagination.limit
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Posts list failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch posts"
        )


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    current_user: Optional[CurrentUser] = Depends(get_optional_user),
    # db: Database = Depends(get_database)  # TODO: Add when database layer is implemented
) -> PostResponse:
    """
    Get post by ID.

    Retrieves full post content and increments view count.
    """
    try:
        logger.info(f"Post request", extra={
            "post_id": post_id,
            "user_id": current_user.user_id if current_user else None
        })

        # TODO: Replace with actual database operations
        # post = await db.posts.find_one({"_id": post_id})
        # if not post:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail="Post not found"
        #     )

        # Check if post is published (unless user is author or admin)
        # if not post["is_published"] and (
        #     not current_user or
        #     (current_user.user_id != post["author_id"] and not current_user.has_permission("admin"))
        # ):
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail="Post not found"
        #     )

        # Increment view count
        # await db.posts.update_one({"_id": post_id}, {"$inc": {"views_count": 1}})

        # Check if user liked the post
        # is_liked_by_user = None
        # if current_user:
        #     like = await db.post_likes.find_one({
        #         "post_id": post_id,
        #         "user_id": current_user.user_id
        #     })
        #     is_liked_by_user = like is not None

        if post_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )

        # Mock post data
        return PostResponse(
            id=post_id,
            title="My Awesome Post",
            content="This is the full content of the awesome post with all details...",
            category=CategoryResponse(id=1, name="Technology", slug="technology"),
            author=AuthorResponse(id=1, full_name="John Doe"),
            tags=["tech", "programming"],
            views_count=43,  # Incremented
            likes_count=5,
            comments_count=3,
            is_published=True,
            is_liked_by_user=False if current_user else None,
            created_at="01.01.2024",
            updated_at="15.01.2024"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Post fetch failed: {str(e)}", extra={"post_id": post_id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch post"
        )


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    request: PostUpdateRequest,
    current_user: CurrentUser = Depends(get_current_user),
    # db: Database = Depends(get_database)  # TODO: Add when database layer is implemented
) -> PostResponse:
    """
    Update post by ID.

    Updates post content and metadata. Only author or admin can update.
    """
    try:
        logger.info(f"Post update request", extra={
            "post_id": post_id,
            "user_id": current_user.user_id
        })

        # TODO: Replace with actual database operations
        # post = await db.posts.find_one({"_id": post_id})
        # if not post:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail="Post not found"
        #     )

        # Check permissions (author or admin)
        # if post["author_id"] != current_user.user_id and not current_user.has_permission("admin"):
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="Not authorized to update this post"
        #     )

        # Build update data
        # update_data = {}
        # if request.title is not None:
        #     update_data["title"] = request.title
        # if request.content is not None:
        #     update_data["content"] = request.content
        # if request.category_id is not None:
        #     update_data["category_id"] = request.category_id
        # if request.tags is not None:
        #     update_data["tags"] = request.tags
        # if request.is_published is not None:
        #     update_data["is_published"] = request.is_published

        # if update_data:
        #     update_data["updated_at"] = datetime.utcnow()
        #     await db.posts.update_one({"_id": post_id}, {"$set": update_data})

        logger.info(f"Post updated successfully", extra={
            "post_id": post_id,
            "user_id": current_user.user_id
        })

        return PostResponse(
            id=post_id,
            title=request.title or "My Awesome Post",
            content=request.content or "This is the updated post content...",
            category=CategoryResponse(id=1, name="Technology", slug="technology") if request.category_id else None,
            author=AuthorResponse(id=current_user.user_id, full_name="John Doe"),
            tags=request.tags or ["tech", "programming"],
            views_count=43,
            likes_count=5,
            comments_count=3,
            is_published=request.is_published if request.is_published is not None else True,
            is_liked_by_user=False,
            created_at="01.01.2024",
            updated_at="15.01.2024"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Post update failed: {str(e)}", extra={
            "post_id": post_id,
            "user_id": current_user.user_id
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update post"
        )


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    # db: Database = Depends(get_database)  # TODO: Add when database layer is implemented
) -> None:
    """
    Delete post by ID.

    Permanently removes post. Only author or admin can delete.
    """
    try:
        logger.info(f"Post deletion request", extra={
            "post_id": post_id,
            "user_id": current_user.user_id
        })

        # TODO: Replace with actual database operations
        # post = await db.posts.find_one({"_id": post_id})
        # if not post:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail="Post not found"
        #     )

        # Check permissions (author or admin)
        # if post["author_id"] != current_user.user_id and not current_user.has_permission("admin"):
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="Not authorized to delete this post"
        #     )

        # Delete post and related data
        # await db.posts.delete_one({"_id": post_id})
        # await db.post_likes.delete_many({"post_id": post_id})
        # await db.comments.delete_many({"post_id": post_id})

        logger.info(f"Post deleted successfully", extra={
            "post_id": post_id,
            "user_id": current_user.user_id
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Post deletion failed: {str(e)}", extra={
            "post_id": post_id,
            "user_id": current_user.user_id
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete post"
        )


@router.post("/{post_id}/like")
async def toggle_post_like(
    post_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    # db: Database = Depends(get_database)  # TODO: Add when database layer is implemented
) -> dict:
    """
    Toggle like status for a post.

    Adds or removes like for the current user.
    """
    try:
        logger.info(f"Post like toggle", extra={
            "post_id": post_id,
            "user_id": current_user.user_id
        })

        # TODO: Replace with actual database operations
        # Check if post exists
        # post = await db.posts.find_one({"_id": post_id})
        # if not post or not post["is_published"]:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail="Post not found"
        #     )

        # Check if user already liked the post
        # existing_like = await db.post_likes.find_one({
        #     "post_id": post_id,
        #     "user_id": current_user.user_id
        # })

        # if existing_like:
        #     # Remove like
        #     await db.post_likes.delete_one({"_id": existing_like["_id"]})
        #     await db.posts.update_one({"_id": post_id}, {"$inc": {"likes_count": -1}})
        #     action = "unliked"
        # else:
        #     # Add like
        #     await db.post_likes.insert_one({
        #         "post_id": post_id,
        #         "user_id": current_user.user_id,
        #         "created_at": datetime.utcnow()
        #     })
        #     await db.posts.update_one({"_id": post_id}, {"$inc": {"likes_count": 1}})
        #     action = "liked"

        # Mock toggle behavior
        action = "liked"

        logger.info(f"Post like toggled", extra={
            "post_id": post_id,
            "user_id": current_user.user_id,
            "action": action
        })

        return {"message": f"Post {action} successfully", "action": action}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Post like toggle failed: {str(e)}", extra={
            "post_id": post_id,
            "user_id": current_user.user_id
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to toggle post like"
        )