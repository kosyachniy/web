import { Post, PostsGetRequest, PostsGetResponse } from '@/types/post';

const API_BASE_URL = process.env.NEXT_PUBLIC_API || 'http://api:5000/';

class ApiError extends Error {
    constructor(public status: number, message: string) {
        super(message);
        this.name = 'ApiError';
    }
}

async function fetchApi<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;

    const response = await fetch(url, {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers,
        },
        ...options,
    });

    if (!response.ok) {
        throw new ApiError(response.status, `HTTP error! status: ${response.status}`);
    }

    return response.json();
}

export async function getPosts(params: PostsGetRequest = {}): Promise<PostsGetResponse> {
    return fetchApi<PostsGetResponse>('/posts/get/', {
        method: 'POST',
        body: JSON.stringify({
            limit: 12,
            ...params,
        }),
    });
}

export async function getPost(id: number): Promise<Post> {
    const response = await getPosts({ id });
    if (!response.posts || response.posts.length === 0) {
        throw new Error('Post not found');
    }
    return response.posts[0];
}
