export interface Post {
    id: number;
    title: string;
    description?: string;
    data: string;
    image?: string;
    url: string;
    created: number;
    updated: number;
    status: number;
    category?: number;
    locale?: string;
    user?: number;

    // Extended fields (when fetching single post)
    category_data?: {
        id: number;
        url: string;
        title: string;
        parents?: Array<{
            id: number;
            url: string;
            title: string;
        }>;
    };
    author?: {
        id: number;
        login: string;
        name?: string;
        surname?: string;
        title?: string;
        image?: string;
    };
    comments?: Array<{
        id: number;
        data: string;
        created: number;
        user?: {
            id: number;
            name?: string;
            surname?: string;
            title?: string;
            image?: string;
        };
    }>;
    views?: number;
}

export interface PostsGetRequest {
    id?: number | number[];
    limit?: number;
    offset?: number;
    search?: string;
    my?: boolean;
    category?: number;
    locale?: string;
    utm?: string;
}

export interface PostsGetResponse {
    posts: Post[];
    count?: number;
}
