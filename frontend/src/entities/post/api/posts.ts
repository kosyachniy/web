import { Post, PostsGetRequest, PostsGetResponse } from '../model/post';
import { api } from '@/shared/services/api/client';
import { shouldUseMockFallback, logApiWarning, addMockDelay } from '@/shared/config/api';
import { getCategories } from '@/entities/category/api/categoryApi';
import type { Category } from '@/entities/category/model/category';

// Cache for categories to avoid repeated API calls
let categoriesCache: Category[] | null = null;

// Function to get categories (with caching)
async function getCachedCategories(): Promise<Category[]> {
    if (!categoriesCache) {
        categoriesCache = await getCategories();
    }
    return categoriesCache;
}

// Helper function to find category by ID recursively
function findCategoryById(categories: Category[], categoryId: number): Category | null {
    for (const category of categories) {
        if (category.id === categoryId) {
            return category;
        }
        if (category.categories && category.categories.length > 0) {
            const found = findCategoryById(category.categories, categoryId);
            if (found) return found;
        }
    }
    return null;
}

// Function to enrich posts with category data
async function enrichPostsWithCategoryData(posts: Post[]): Promise<Post[]> {
    const categories = await getCachedCategories();
    
    return posts.map(post => {
        if (!post.category) return post;
        
        const category = findCategoryById(categories, post.category);
        if (!category) return post;
        
        return {
            ...post,
            category_data: {
                id: category.id,
                url: category.url,
                title: category.title,
                parents: category.parents
            }
        };
    });
}

export async function getPosts(params: PostsGetRequest = {}): Promise<PostsGetResponse> {
    if (shouldUseMockFallback()) {
        try {
            const response = await api.post<PostsGetResponse>('/posts/get/', {
                limit: 12,
                ...params,
            });
            
            return {
                ...response,
                posts: await enrichPostsWithCategoryData(response.posts)
            };
        } catch (error) {
            logApiWarning('Posts API not available', error);
            await addMockDelay();
            
            return {
                posts: [],
                count: 0
            };
        }
    } else {
        // Production mode - let the error bubble up
        const response = await api.post<PostsGetResponse>('/posts/get/', {
            limit: 12,
            ...params,
        });
        
        return {
            ...response,
            posts: await enrichPostsWithCategoryData(response.posts)
        };
    }
}

export async function getPost(id: number): Promise<Post> {
    const response = await getPosts({ id });
    if (!response.posts || response.posts.length === 0) {
        throw new Error('Post not found');
    }
    return response.posts[0];
}

export async function createPost(postData: Partial<Post>): Promise<Post> {
    return api.post<Post>('/posts/', postData);
}

export async function updatePost(id: number, postData: Partial<Post>): Promise<Post> {
    return api.put<Post>(`/posts/${id}/`, postData);
}

export async function deletePost(id: number): Promise<void> {
    return api.delete(`/posts/${id}/`);
}
