"""
Categories management endpoints.

Provides CRUD operations for post categories, including hierarchical
category support and category-based post statistics.
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.api.deps.auth import get_current_user, require_permissions, CurrentUser
from app.api.deps.pagination import PaginationParams, PaginatedResponse
from app.core import get_logger

logger = get_logger(__name__)
router = APIRouter()


# Request/Response Models
class CategoryCreateRequest(BaseModel):
    """Category creation request model."""
    name: str = Field(min_length=1, max_length=100, description="Category name", example="Technology")
    description: Optional[str] = Field(None, max_length=500, description="Category description", example="All tech-related posts")
    parent_id: Optional[int] = Field(None, gt=0, description="Parent category ID for hierarchical structure", example=1)
    color: Optional[str] = Field(None, regex=r"^#[0-9A-Fa-f]{6}$", description="Hex color code", example="#3B82F6")
    icon: Optional[str] = Field(None, max_length=50, description="Icon name or class", example="tech-icon")


class CategoryUpdateRequest(BaseModel):
    """Category update request model."""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Category name", example="Technology")
    description: Optional[str] = Field(None, max_length=500, description="Category description", example="All tech-related posts")
    parent_id: Optional[int] = Field(None, gt=0, description="Parent category ID", example=1)
    color: Optional[str] = Field(None, regex=r"^#[0-9A-Fa-f]{6}$", description="Hex color code", example="#3B82F6")
    icon: Optional[str] = Field(None, max_length=50, description="Icon name or class", example="tech-icon")


class CategoryResponse(BaseModel):
    """Category response model."""
    id: int = Field(description="Category ID", example=1)
    name: str = Field(description="Category name", example="Technology")
    slug: str = Field(description="Category URL slug", example="technology")
    description: Optional[str] = Field(None, description="Category description", example="All tech-related posts")
    parent_id: Optional[int] = Field(None, description="Parent category ID", example=1)
    color: Optional[str] = Field(None, description="Hex color code", example="#3B82F6")
    icon: Optional[str] = Field(None, description="Icon name or class", example="tech-icon")
    posts_count: int = Field(default=0, description="Number of posts in category", example=42)
    is_active: bool = Field(default=True, description="Category status", example=True)
    created_at: str = Field(description="Creation date (DD.MM.YYYY)", example="01.01.2024")
    updated_at: Optional[str] = Field(None, description="Last update date (DD.MM.YYYY)", example="15.01.2024")


class CategoryTreeResponse(BaseModel):
    """Hierarchical category tree response model."""
    id: int = Field(description="Category ID", example=1)
    name: str = Field(description="Category name", example="Technology")
    slug: str = Field(description="Category URL slug", example="technology")
    description: Optional[str] = Field(None, description="Category description", example="All tech-related posts")
    color: Optional[str] = Field(None, description="Hex color code", example="#3B82F6")
    icon: Optional[str] = Field(None, description="Icon name or class", example="tech-icon")
    posts_count: int = Field(default=0, description="Number of posts in category", example=42)
    children: List["CategoryTreeResponse"] = Field(default=[], description="Subcategories")


class CategoryStatsResponse(BaseModel):
    """Category statistics response model."""
    id: int = Field(description="Category ID", example=1)
    name: str = Field(description="Category name", example="Technology")
    posts_count: int = Field(description="Total posts", example=42)
    published_posts_count: int = Field(description="Published posts", example=38)
    draft_posts_count: int = Field(description="Draft posts", example=4)
    total_views: int = Field(description="Total views across all posts", example=1500)
    total_likes: int = Field(description="Total likes across all posts", example=150)
    avg_views_per_post: float = Field(description="Average views per post", example=35.7)
    last_post_date: Optional[str] = Field(None, description="Last post date (DD.MM.YYYY)", example="15.01.2024")


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    request: CategoryCreateRequest,
    current_user: CurrentUser = Depends(require_permissions(["admin", "category_management"])),
    # db: Database = Depends(get_database)  # TODO: Add when database layer is implemented
) -> CategoryResponse:
    """
    Create a new category.

    Creates a new post category with optional hierarchical structure.
    Requires admin or category management permissions.
    """
    try:
        logger.info(f"Creating category", extra={
            "user_id": current_user.user_id,
            "name": request.name,
            "parent_id": request.parent_id
        })

        # TODO: Replace with actual database operations
        # Check if parent category exists
        # if request.parent_id:
        #     parent = await db.categories.find_one({"_id": request.parent_id})
        #     if not parent:
        #         raise HTTPException(
        #             status_code=status.HTTP_400_BAD_REQUEST,
        #             detail="Parent category not found"
        #         )

        # Generate slug from name
        # slug = request.name.lower().replace(" ", "-").replace("_", "-")
        # slug = re.sub(r'[^a-z0-9-]', '', slug)

        # Check if category with same name/slug exists
        # existing = await db.categories.find_one({
        #     "$or": [
        #         {"name": request.name},
        #         {"slug": slug}
        #     ]
        # })
        # if existing:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Category with this name already exists"
        #     )

        # Create category document
        # category_data = {
        #     "name": request.name,
        #     "slug": slug,
        #     "description": request.description,
        #     "parent_id": request.parent_id,
        #     "color": request.color,
        #     "icon": request.icon,
        #     "posts_count": 0,
        #     "is_active": True,
        #     "created_at": datetime.utcnow(),
        #     "updated_at": datetime.utcnow()
        # }

        # result = await db.categories.insert_one(category_data)
        # category_id = result.inserted_id

        # Mock category data
        category_id = 1
        slug = request.name.lower().replace(" ", "-")

        logger.info(f"Category created successfully", extra={
            "category_id": category_id,
            "user_id": current_user.user_id
        })

        return CategoryResponse(
            id=category_id,
            name=request.name,
            slug=slug,
            description=request.description,
            parent_id=request.parent_id,
            color=request.color,
            icon=request.icon,
            posts_count=0,
            is_active=True,
            created_at="15.01.2024"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Category creation failed: {str(e)}", extra={"user_id": current_user.user_id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create category"
        )


@router.get("/", response_model=PaginatedResponse[CategoryResponse])
async def list_categories(
    pagination: PaginationParams = Depends(),
    parent_id: Optional[int] = Query(None, description="Filter by parent category ID"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    search: Optional[str] = Query(None, description="Search categories by name"),
    include_stats: bool = Query(False, description="Include post count statistics"),
    # db: Database = Depends(get_database)  # TODO: Add when database layer is implemented
) -> PaginatedResponse[CategoryResponse]:
    """
    List categories with filtering and pagination.

    Supports filtering by parent category, status, and search queries.
    """
    try:
        logger.info(f"Categories list request", extra={
            "parent_id": parent_id,
            "search": search,
            "include_stats": include_stats,
            "pagination": {"offset": pagination.offset, "limit": pagination.limit}
        })

        # TODO: Replace with actual database operations
        # Build filter query
        # filter_query = {}
        # if parent_id is not None:
        #     filter_query["parent_id"] = parent_id
        # if is_active is not None:
        #     filter_query["is_active"] = is_active
        # if search:
        #     filter_query["name"] = {"$regex": search, "$options": "i"}

        # Get total count and categories
        # total_count = await db.categories.count_documents(filter_query)
        # categories_cursor = db.categories.find(filter_query).skip(pagination.offset).limit(pagination.limit)
        # categories = await categories_cursor.to_list(length=pagination.limit)

        # Update post counts if requested
        # if include_stats:
        #     for category in categories:
        #         posts_count = await db.posts.count_documents({
        #             "category_id": category["_id"],
        #             "is_published": True
        #         })
        #         await db.categories.update_one(
        #             {"_id": category["_id"]},
        #             {"$set": {"posts_count": posts_count}}
        #         )
        #         category["posts_count"] = posts_count

        # Mock categories data
        mock_categories = [
            CategoryResponse(
                id=1,
                name="Technology",
                slug="technology",
                description="All tech-related posts",
                parent_id=None,
                color="#3B82F6",
                icon="tech-icon",
                posts_count=15,
                is_active=True,
                created_at="01.01.2024",
                updated_at="15.01.2024"
            ),
            CategoryResponse(
                id=2,
                name="Design",
                slug="design",
                description="Design and UI/UX posts",
                parent_id=None,
                color="#8B5CF6",
                icon="design-icon",
                posts_count=8,
                is_active=True,
                created_at="02.01.2024"
            ),
            CategoryResponse(
                id=3,
                name="Programming",
                slug="programming",
                description="Programming tutorials and tips",
                parent_id=1,  # Child of Technology
                color="#10B981",
                icon="code-icon",
                posts_count=12,
                is_active=True,
                created_at="03.01.2024"
            )
        ]

        # Filter by parent_id if specified
        if parent_id is not None:
            mock_categories = [cat for cat in mock_categories if cat.parent_id == parent_id]

        return PaginatedResponse(
            items=mock_categories,
            total=len(mock_categories),
            offset=pagination.offset,
            limit=pagination.limit
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Categories list failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch categories"
        )


@router.get("/tree", response_model=List[CategoryTreeResponse])
async def get_category_tree(
    include_inactive: bool = Query(False, description="Include inactive categories"),
    # db: Database = Depends(get_database)  # TODO: Add when database layer is implemented
) -> List[CategoryTreeResponse]:
    """
    Get hierarchical category tree.

    Returns all categories organized in a tree structure.
    """
    try:
        logger.info(f"Category tree request", extra={"include_inactive": include_inactive})

        # TODO: Replace with actual database operations
        # Build filter query
        # filter_query = {}
        # if not include_inactive:
        #     filter_query["is_active"] = True

        # Get all categories
        # categories = await db.categories.find(filter_query).to_list(length=None)

        # Build hierarchical structure
        # def build_tree(parent_id=None):
        #     tree = []
        #     for category in categories:
        #         if category.get("parent_id") == parent_id:
        #             category_node = CategoryTreeResponse(**category)
        #             category_node.children = build_tree(category["_id"])
        #             tree.append(category_node)
        #     return tree

        # Mock hierarchical data
        mock_tree = [
            CategoryTreeResponse(
                id=1,
                name="Technology",
                slug="technology",
                description="All tech-related posts",
                color="#3B82F6",
                icon="tech-icon",
                posts_count=15,
                children=[
                    CategoryTreeResponse(
                        id=3,
                        name="Programming",
                        slug="programming",
                        description="Programming tutorials and tips",
                        color="#10B981",
                        icon="code-icon",
                        posts_count=12,
                        children=[]
                    ),
                    CategoryTreeResponse(
                        id=4,
                        name="AI & ML",
                        slug="ai-ml",
                        description="Artificial Intelligence and Machine Learning",
                        color="#F59E0B",
                        icon="ai-icon",
                        posts_count=3,
                        children=[]
                    )
                ]
            ),
            CategoryTreeResponse(
                id=2,
                name="Design",
                slug="design",
                description="Design and UI/UX posts",
                color="#8B5CF6",
                icon="design-icon",
                posts_count=8,
                children=[]
            )
        ]

        return mock_tree

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Category tree failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch category tree"
        )


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int,
    # db: Database = Depends(get_database)  # TODO: Add when database layer is implemented
) -> CategoryResponse:
    """
    Get category by ID.

    Retrieves detailed information about a specific category.
    """
    try:
        logger.info(f"Category request", extra={"category_id": category_id})

        # TODO: Replace with actual database operations
        # category = await db.categories.find_one({"_id": category_id})
        # if not category:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail="Category not found"
        #     )

        if category_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

        # Mock category data
        return CategoryResponse(
            id=category_id,
            name="Technology",
            slug="technology",
            description="All tech-related posts",
            parent_id=None,
            color="#3B82F6",
            icon="tech-icon",
            posts_count=15,
            is_active=True,
            created_at="01.01.2024",
            updated_at="15.01.2024"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Category fetch failed: {str(e)}", extra={"category_id": category_id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch category"
        )


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    request: CategoryUpdateRequest,
    current_user: CurrentUser = Depends(require_permissions(["admin", "category_management"])),
    # db: Database = Depends(get_database)  # TODO: Add when database layer is implemented
) -> CategoryResponse:
    """
    Update category by ID.

    Updates category information. Requires admin or category management permissions.
    """
    try:
        logger.info(f"Category update request", extra={
            "category_id": category_id,
            "user_id": current_user.user_id
        })

        # TODO: Replace with actual database operations
        # category = await db.categories.find_one({"_id": category_id})
        # if not category:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail="Category not found"
        #     )

        # Build update data
        # update_data = {}
        # if request.name is not None:
        #     # Check for duplicate names
        #     existing = await db.categories.find_one({
        #         "name": request.name,
        #         "_id": {"$ne": category_id}
        #     })
        #     if existing:
        #         raise HTTPException(
        #             status_code=status.HTTP_400_BAD_REQUEST,
        #             detail="Category with this name already exists"
        #         )
        #     update_data["name"] = request.name
        #     update_data["slug"] = request.name.lower().replace(" ", "-")

        # if request.description is not None:
        #     update_data["description"] = request.description
        # if request.parent_id is not None:
        #     update_data["parent_id"] = request.parent_id
        # if request.color is not None:
        #     update_data["color"] = request.color
        # if request.icon is not None:
        #     update_data["icon"] = request.icon

        # if update_data:
        #     update_data["updated_at"] = datetime.utcnow()
        #     await db.categories.update_one({"_id": category_id}, {"$set": update_data})

        logger.info(f"Category updated successfully", extra={
            "category_id": category_id,
            "user_id": current_user.user_id
        })

        return CategoryResponse(
            id=category_id,
            name=request.name or "Technology",
            slug=(request.name or "Technology").lower().replace(" ", "-"),
            description=request.description,
            parent_id=request.parent_id,
            color=request.color or "#3B82F6",
            icon=request.icon or "tech-icon",
            posts_count=15,
            is_active=True,
            created_at="01.01.2024",
            updated_at="15.01.2024"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Category update failed: {str(e)}", extra={
            "category_id": category_id,
            "user_id": current_user.user_id
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update category"
        )


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    force: bool = Query(False, description="Force deletion even if category has posts"),
    current_user: CurrentUser = Depends(require_permissions(["admin", "category_management"])),
    # db: Database = Depends(get_database)  # TODO: Add when database layer is implemented
) -> None:
    """
    Delete category by ID.

    Removes category. Fails if category has posts unless force=true.
    Requires admin or category management permissions.
    """
    try:
        logger.info(f"Category deletion request", extra={
            "category_id": category_id,
            "force": force,
            "user_id": current_user.user_id
        })

        # TODO: Replace with actual database operations
        # category = await db.categories.find_one({"_id": category_id})
        # if not category:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail="Category not found"
        #     )

        # Check if category has posts
        # posts_count = await db.posts.count_documents({"category_id": category_id})
        # if posts_count > 0 and not force:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail=f"Category has {posts_count} posts. Use force=true to delete anyway."
        #     )

        # Check if category has subcategories
        # subcategories_count = await db.categories.count_documents({"parent_id": category_id})
        # if subcategories_count > 0 and not force:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail=f"Category has {subcategories_count} subcategories. Use force=true to delete anyway."
        #     )

        # Delete category and update related data
        # if force:
        #     # Move posts to null category or delete them
        #     await db.posts.update_many(
        #         {"category_id": category_id},
        #         {"$unset": {"category_id": ""}}
        #     )
        #     # Move subcategories to parent category
        #     await db.categories.update_many(
        #         {"parent_id": category_id},
        #         {"$set": {"parent_id": category.get("parent_id")}}
        #     )

        # await db.categories.delete_one({"_id": category_id})

        logger.info(f"Category deleted successfully", extra={
            "category_id": category_id,
            "user_id": current_user.user_id
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Category deletion failed: {str(e)}", extra={
            "category_id": category_id,
            "user_id": current_user.user_id
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete category"
        )


@router.get("/{category_id}/stats", response_model=CategoryStatsResponse)
async def get_category_stats(
    category_id: int,
    current_user: CurrentUser = Depends(require_permissions(["admin", "category_management"])),
    # db: Database = Depends(get_database)  # TODO: Add when database layer is implemented
) -> CategoryStatsResponse:
    """
    Get detailed statistics for a category.

    Returns comprehensive stats including post counts, views, likes, etc.
    Requires admin or category management permissions.
    """
    try:
        logger.info(f"Category stats request", extra={
            "category_id": category_id,
            "user_id": current_user.user_id
        })

        # TODO: Replace with actual database operations
        # category = await db.categories.find_one({"_id": category_id})
        # if not category:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail="Category not found"
        #     )

        # Get post statistics
        # stats_pipeline = [
        #     {"$match": {"category_id": category_id}},
        #     {"$group": {
        #         "_id": None,
        #         "total_posts": {"$sum": 1},
        #         "published_posts": {"$sum": {"$cond": [{"$eq": ["$is_published", True]}, 1, 0]}},
        #         "draft_posts": {"$sum": {"$cond": [{"$eq": ["$is_published", False]}, 1, 0]}},
        #         "total_views": {"$sum": "$views_count"},
        #         "total_likes": {"$sum": "$likes_count"},
        #         "avg_views": {"$avg": "$views_count"}
        #     }}
        # ]

        # stats_result = await db.posts.aggregate(stats_pipeline).to_list(length=1)
        # stats = stats_result[0] if stats_result else {}

        # Get last post date
        # last_post = await db.posts.find_one(
        #     {"category_id": category_id},
        #     sort=[("created_at", -1)]
        # )

        # Mock statistics data
        return CategoryStatsResponse(
            id=category_id,
            name="Technology",
            posts_count=15,
            published_posts_count=12,
            draft_posts_count=3,
            total_views=1500,
            total_likes=150,
            avg_views_per_post=100.0,
            last_post_date="15.01.2024"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Category stats failed: {str(e)}", extra={
            "category_id": category_id,
            "user_id": current_user.user_id
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch category statistics"
        )