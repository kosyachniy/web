'use client';

import { useState, useCallback, useEffect } from 'react';
import { Search, SearchFilters } from '@/shared/ui/search';
import { PostsGrid } from './PostsGrid';
import { Post } from '@/entities/post';
import { getPosts } from '@/entities/post';
import { useToastActions } from '@/shared/hooks/useToast';
import { useTranslations } from 'next-intl';

interface PostsWithSearchProps {
    initialPosts?: Post[];
    categoryId?: number;
    locale?: string;
    limit?: number;
}

export function PostsWithSearch({
    initialPosts = [],
    categoryId,
    locale,
    limit = 12
}: PostsWithSearchProps) {
    const [query, setQuery] = useState('');
    const [filters, setFilters] = useState<SearchFilters>({});
    const [posts, setPosts] = useState<Post[]>(initialPosts);
    const [loading, setLoading] = useState(false);
    const [loadingMore, setLoadingMore] = useState(false);
    const [hasMore, setHasMore] = useState(true);
    const [currentQuery, setCurrentQuery] = useState('');

    const { error: showError } = useToastActions();
    const t = useTranslations('search');

    const loadPosts = useCallback(async (searchQuery: string, searchFilters: SearchFilters, append = false) => {
        try {
            if (!append) {
                setLoading(true);
            } else {
                setLoadingMore(true);
            }

            const response = await getPosts({
                limit,
                category: categoryId,
                locale,
                search: searchQuery || '',
                offset: append ? posts.length : 0,
                // TODO: Add sort and other filter parameters when backend API supports them
                // sort: searchFilters.sort as string | undefined,
            });

            if (append) {
                setPosts(prev => [...prev, ...response.posts]);
            } else {
                setPosts(response.posts);
            }

            // Check if there are more posts to load
            if (response.count !== undefined) {
                const currentOffset = append ? posts.length : 0;
                setHasMore(currentOffset + response.posts.length < response.count);
            } else {
                setHasMore(response.posts.length === limit);
            }

        } catch (err) {
            console.error('Error loading posts:', err);
            const errorMessage = err instanceof Error ? err.message : 'Failed to load posts';
            showError(errorMessage);
        } finally {
            setLoading(false);
            setLoadingMore(false);
        }
    }, [categoryId, locale, limit, posts.length, showError]);

    const handleSearch = useCallback((searchQuery: string, searchFilters: SearchFilters) => {
        setCurrentQuery(searchQuery);
        loadPosts(searchQuery, searchFilters, false);
    }, [loadPosts]);

    const handleLoadMore = useCallback(() => {
        if (!loadingMore && hasMore) {
            loadPosts(currentQuery, filters, true);
        }
    }, [currentQuery, filters, hasMore, loadingMore, loadPosts]);

    // Load initial posts if not provided
    useEffect(() => {
        if (initialPosts.length === 0) {
            loadPosts('', {}, false);
        }
    }, [initialPosts.length, loadPosts]); // Run when dependencies change

    return (
        <div className="space-y-6">
            {/* Search Component */}
            <Search
                value={query}
                onChange={setQuery}
                onSearch={handleSearch}
                placeholder={t('placeholder')}
                filters={filters}
                onFiltersChange={setFilters}
                mode="simple"
                size="default"
                loading={loading}
                className="mb-8"
            />

            {/* Posts Grid */}
            {loading ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 items-start">
                    {Array.from({ length: limit }).map((_, i) => (
                        <div key={i} className="animate-pulse">
                            <div className="bg-gray-200 dark:bg-gray-700 rounded-[1rem] h-64"></div>
                        </div>
                    ))}
                </div>
            ) : (
                <PostsGrid
                    initialPosts={posts}
                    searchQuery={currentQuery}
                    categoryId={categoryId}
                    locale={locale}
                    limit={limit}
                    onLoadMore={handleLoadMore}
                    hasMore={hasMore}
                    loadingMore={loadingMore}
                />
            )}
        </div>
    );
}