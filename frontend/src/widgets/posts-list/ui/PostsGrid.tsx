'use client';

import { useState, useEffect, useCallback } from 'react';
import { PostCard } from './PostCard';
import { Post, PostsGetRequest } from '@/entities/post';
import { getPosts } from '@/entities/post';
import { Button } from '@/shared/ui/button';
import { useToastActions } from '@/shared/hooks/useToast';
import { AlertIcon, SearchIcon, LoadingIcon } from '@/shared/ui/icons';

interface PostsGridProps {
    initialPosts?: Post[];
    searchQuery?: string;
    categoryId?: number;
    locale?: string;
    limit?: number;
    onLoadMore?: () => void;
    hasMore?: boolean;
    loadingMore?: boolean;
}

export function PostsGrid({
    initialPosts = [],
    searchQuery = '',
    categoryId,
    locale,
    limit = 12,
    onLoadMore,
    hasMore = false,
    loadingMore = false
}: PostsGridProps) {
    const [posts, setPosts] = useState<Post[]>(initialPosts);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const { error: showError } = useToastActions();

    const loadPosts = useCallback(async (params: PostsGetRequest = {}, append = false) => {
        try {
            if (!append) {
                setLoading(true);
            }

            setError(null);

            const response = await getPosts({
                limit,
                category: categoryId,
                locale,
                search: searchQuery || '',
                ...params,
            });

            if (append) {
                setPosts(prev => [...prev, ...response.posts]);
            } else {
                setPosts(response.posts);
            }

        } catch (err) {
            console.error('Error loading posts:', err);
            const errorMessage = err instanceof Error ? err.message : 'Failed to load posts';
            setError(errorMessage);
            showError(errorMessage);
        } finally {
            setLoading(false);
        }
    }, [categoryId, locale, limit, searchQuery, showError]);

    // Load more posts handler - delegates to parent
    const handleLoadMore = useCallback(() => {
        onLoadMore?.();
    }, [onLoadMore]);

    // Load posts when dependencies change
    useEffect(() => {
        if (initialPosts.length === 0) {
            loadPosts();
        }
    }, [categoryId, locale, searchQuery, initialPosts.length, loadPosts]);

    if (loading) {
        return (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 items-start">
                {Array.from({ length: limit }).map((_, i) => (
                    <div key={i} className="animate-pulse">
                        <div className="bg-gray-200 dark:bg-gray-700 rounded-[1rem] h-64"></div>
                    </div>
                ))}
            </div>
        );
    }

    if (error && posts.length === 0) {
        return (
            <div className="text-center py-12">
                <div className="text-red-500 mb-4">
                    <AlertIcon size={48} className="mx-auto mb-4" />
                    <p className="text-lg font-medium">Failed to load posts</p>
                    <p className="text-sm text-muted-foreground mt-2">{error}</p>
                </div>
                <Button onClick={() => loadPosts()} variant="outline">
                    Try Again
                </Button>
            </div>
        );
    }

    if (posts.length === 0) {
        return (
            <div className="text-center py-12">
                <div className="text-muted-foreground">
                    <SearchIcon size={48} className="mx-auto mb-4" />
                    <p className="text-lg">No posts found</p>
                    {searchQuery && (
                        <p className="text-sm mt-2">
                            Try adjusting your search terms
                        </p>
                    )}
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 items-start">
                {posts.map((post) => (
                    <PostCard key={post.id} post={post} />
                ))}
            </div>

            {hasMore && (
                <div className="text-center pt-8">
                    <Button
                        onClick={handleLoadMore}
                        disabled={loadingMore}
                        variant="outline"
                        className="min-w-32"
                    >
                        {loadingMore ? (
                            <>
                                <LoadingIcon size={16} className="animate-spin -ml-1 mr-2" />
                                Loading...
                            </>
                        ) : (
                            'Load More'
                        )}
                    </Button>
                </div>
            )}
        </div>
    );
}
