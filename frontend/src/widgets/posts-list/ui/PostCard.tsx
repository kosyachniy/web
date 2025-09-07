'use client';

import React, { useState } from 'react';
import { Card } from '@/shared/ui/card';
import { Post } from '@/entities/post';
import { EyeIcon, UserIcon, CalendarIcon, TagIcon } from '@/shared/ui/icons';
import { formatDate } from '@/shared/lib/date';
import Image from 'next/image';

interface PostCardProps {
    post: Post;
}

export function PostCard({ post }: PostCardProps) {
    // Like functionality - in production this would come from props or global state
    const [isLiked, setIsLiked] = useState(false);

    const stripHtml = (html: string) => {
        return html.replace(/<[^>]*>/g, '').substring(0, 150);
    };

    const handleLikeClick = (id?: string | number) => {
        // In production, this would call an API to like/unlike the post
        console.log('Like clicked for post:', id);
        setIsLiked(prev => !prev);
        
        // TODO: Integrate with API
        // Example:
        // await togglePostLike(post.id);
    };

    // Prepare filters for above title
    const filters = [];

    // Add category to filters if available
    if (post.category_data) {
        filters.push({
            icon: <TagIcon size={12} />,
            value: post.category_data.title
        });
    }

    // Add views to filters if available
    if (post.views) {
        filters.push({
            icon: <EyeIcon size={12} />,
            value: post.views.toString()
        });
    }

    filters.push({
        icon: <CalendarIcon size={12} />,
        value: formatDate(post.created)
    });

    // Prepare metadata for bottom (author only)
    const metadata: Array<{
        icon?: React.ReactNode;
        label: string;
        value: string | number;
    }> = [];
    if (post.author) {
        metadata.push({
            icon: post.author.image ? (
                <Image
                    src={post.author.image}
                    alt={post.author.name || post.author.login}
                    width={12}
                    height={12}
                    className="rounded-full"
                />
            ) : <UserIcon size={12} />,
            label: 'Author',
            value: post.author.name || post.author.login
        });
    }

    return (
        <Card
            title={post.title}
            description={post.description || stripHtml(post.data)}
            images={post.image ? [post.image] : []}
            href={`/posts/${post.url}`}
            filters={filters}
            metadata={metadata}
            variant="default"
            showLikeButton={true}
            isLiked={isLiked}
            onLikeClick={handleLikeClick}
            id={post.id}
        />
    );
}
