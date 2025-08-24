import { Post, PostsGetRequest, PostsGetResponse } from '../model/post';
import { api } from '@/shared/services/api/client';

export async function getPosts(params: PostsGetRequest = {}): Promise<PostsGetResponse> {
    return api.post<PostsGetResponse>('/posts/get/', {
        limit: 12,
        ...params,
    });
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
