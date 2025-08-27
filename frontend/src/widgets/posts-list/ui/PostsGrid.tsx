'use client';

import { useState, useEffect, useMemo, useCallback } from 'react';
import { PostCard } from './PostCard';
import { Post, PostsGetRequest } from '@/entities/post';
import { getPosts } from '@/entities/post';
import { Button } from '@/shared/ui/button';
import { Input } from '@/shared/ui/input';
import { useToastActions } from '@/shared/hooks/useToast';

interface PostsGridProps {
    initialPosts?: Post[];
    searchable?: boolean;
    categoryId?: number;
    locale?: string;
    limit?: number;
}

export function PostsGrid({
    initialPosts = [],
    searchable = true,
    categoryId,
    locale,
    limit = 12
}: PostsGridProps) {
    const [posts, setPosts] = useState<Post[]>(initialPosts);
    const [loading, setLoading] = useState(false);
    const [loadingMore, setLoadingMore] = useState(false);
    const [search, setSearch] = useState('');
    
    const searchValue = useMemo(() => search || '', [search]);
    const [hasMore, setHasMore] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const { error: showError } = useToastActions();

    const loadPosts = useCallback(async (params: PostsGetRequest = {}, append = false) => {
        try {
            if (!append) {
                setLoading(true);
            } else {
                setLoadingMore(true);
            }

            setError(null);

            const response = await getPosts({
                limit,
                category: categoryId,
                locale,
                ...params,
            });

            if (append) {
                setPosts(prev => [...prev, ...response.posts]);
            } else {
                setPosts(response.posts);
            }

            // Check if there are more posts to load
            if (response.count !== undefined) {
                const currentOffset = params.offset || 0;
                setHasMore(currentOffset + response.posts.length < response.count);
            } else {
                // If no count provided, assume no more if we got less than requested
                setHasMore(response.posts.length === limit);
            }

        } catch (err) {
            console.error('Error loading posts:', err);
            const errorMessage = err instanceof Error ? err.message : 'Failed to load posts';
            setError(errorMessage);
            showError(errorMessage);
        } finally {
            setLoading(false);
            setLoadingMore(false);
        }
    }, [categoryId, locale, limit, showError]);

    const handleSearch = (searchTerm: string) => {
        setSearch(searchTerm);
        loadPosts({ search: searchTerm, offset: 0 });
    };

    const loadMore = () => {
        if (!loadingMore && hasMore) {
            loadPosts({
                search: search || '',
                offset: posts.length
            }, true);
        }
    };

    // Load initial posts if not provided and reset search when category or locale changes
    useEffect(() => {
        // Only reset search if categoryId is defined (not on initial render with undefined categoryId)
        if (categoryId !== undefined) {
            setSearch('');
        }
        if (initialPosts.length === 0) {
            loadPosts();
        }
    }, [categoryId, locale, initialPosts.length, loadPosts]);

    if (loading) {
        return (
            <div className="space-y-6">
                {searchable && (
                    <div className="max-w-md">
                        <Input
                            placeholder="Search posts..."
                            disabled
                            className="w-full"
                        />
                    </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {Array.from({ length: limit }).map((_, i) => (
                        <div key={i} className="animate-pulse">
                            <div className="bg-gray-200 dark:bg-gray-700 rounded-[1rem] h-64"></div>
                        </div>
                    ))}
                </div>
            </div>
        );
    }

    if (error && posts.length === 0) {
        return (
            <div className="text-center py-12">
                <div className="text-red-500 mb-4">
                    <svg className="w-12 h-12 mx-auto mb-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <circle cx="12" cy="12" r="10" />
                        <line x1="12" y1="8" x2="12" y2="12" />
                        <line x1="12" y1="16" x2="12.01" y2="16" />
                    </svg>
                    <p className="text-lg font-medium">Failed to load posts</p>
                    <p className="text-sm text-muted-foreground mt-2">{error}</p>
                </div>
                <Button onClick={() => loadPosts()} variant="outline">
                    Try Again
                </Button>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {searchable && (
                <div className="max-w-md">
                    <Input
                        placeholder="Search posts..."
                        value={searchValue}
                        onChange={(e) => handleSearch(e.target.value)}
                        className="w-full"
                    />
                </div>
            )}

            {posts.length === 0 ? (
                <div className="text-center py-12">
                    <div className="text-muted-foreground">
                        <svg className="w-12 h-12 mx-auto mb-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <circle cx="11" cy="11" r="8" />
                            <path d="m21 21-4.35-4.35" />
                        </svg>
                        <p className="text-lg">No posts found</p>
                        {search && (
                            <p className="text-sm mt-2">
                                Try adjusting your search terms or{' '}
                                <button
                                    onClick={() => handleSearch('')}
                                    className="text-primary hover:underline"
                                >
                                    clear the search
                                </button>
                            </p>
                        )}
                    </div>
                </div>
            ) : (
                <>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {posts.map((post) => (
                            <PostCard key={post.id} post={post} />
                        ))}
                    </div>

                    {hasMore && (
                        <div className="text-center pt-8">
                            <Button
                                onClick={loadMore}
                                disabled={loadingMore}
                                variant="outline"
                                className="min-w-32"
                            >
                                {loadingMore ? (
                                    <>
                                        <svg className="animate-spin -ml-1 mr-2 h-4 w-4" viewBox="0 0 24 24">
                                            <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" className="opacity-25" />
                                            <path fill="currentColor" className="opacity-75" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                                        </svg>
                                        Loading...
                                    </>
                                ) : (
                                    'Load More'
                                )}
                            </Button>
                        </div>
                    )}
                </>
            )}
        </div>
    );
}
