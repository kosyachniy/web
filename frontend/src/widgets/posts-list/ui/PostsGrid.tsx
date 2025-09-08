'use client';

import { useState, useEffect, useMemo, useCallback } from 'react';
import { PostCard } from './PostCard';
import { Post, PostsGetRequest } from '@/entities/post';
import { getPosts } from '@/entities/post';
import { Button } from '@/shared/ui/button';
import { Input } from '@/shared/ui/input';
import { useToastActions } from '@/shared/hooks/useToast';
import { AlertIcon, SearchIcon, LoadingIcon } from '@/shared/ui/icons';

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

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 items-start">
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
                        <SearchIcon size={48} className="mx-auto mb-4" />
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
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 items-start">
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
                                        <LoadingIcon size={16} className="animate-spin -ml-1 mr-2" />
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
