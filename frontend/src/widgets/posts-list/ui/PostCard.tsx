'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/shared/ui/card';
import { Post } from '@/entities/post';
import Image from 'next/image';
import Link from 'next/link';

interface PostCardProps {
    post: Post;
}

export function PostCard({ post }: PostCardProps) {
    const formatDate = (timestamp: number) => {
        return new Date(timestamp * 1000).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
        });
    };

    const stripHtml = (html: string) => {
        return html.replace(/<[^>]*>/g, '').substring(0, 150);
    };

    return (
        <Link href={`/posts/${post.url}`} className="block group">
            <Card className="h-full overflow-hidden hover:shadow-lg transition-all duration-200 group-hover:scale-[1.02]">
                {post.image && (
                    <div className="relative w-full h-48 overflow-hidden">
                        <Image
                            src={post.image}
                            alt={post.title}
                            fill
                            className="object-cover transition-transform duration-200 group-hover:scale-105"
                            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                        />
                    </div>
                )}

                <CardHeader className="pb-2">
                    <CardTitle className="text-lg font-semibold line-clamp-2 group-hover:text-primary transition-colors">
                        {post.title}
                    </CardTitle>

                    {post.category_data && (
                        <div className="flex items-center gap-2 text-sm text-muted-foreground">
                            <span className="bg-primary/10 text-primary px-2 py-1 rounded-full text-xs">
                                {post.category_data.title}
                            </span>
                        </div>
                    )}
                </CardHeader>

                <CardContent className="pt-0">
                    <p className="text-sm text-muted-foreground line-clamp-3 mb-4">
                        {post.description || stripHtml(post.data)}
                    </p>

                    <div className="flex items-center justify-between text-xs text-muted-foreground">
                        <div className="flex items-center gap-4">
                            <span>{formatDate(post.created)}</span>

                            {post.author && (
                                <span className="flex items-center gap-1">
                                    {post.author.image && (
                                        <Image
                                            src={post.author.image}
                                            alt={post.author.name || post.author.login}
                                            width={16}
                                            height={16}
                                            className="rounded-full"
                                        />
                                    )}
                                    {post.author.name || post.author.login}
                                </span>
                            )}
                        </div>

                        {post.views && (
                            <span className="flex items-center gap-1">
                                <svg className="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                                    <circle cx="12" cy="12" r="3" />
                                </svg>
                                {post.views}
                            </span>
                        )}
                    </div>
                </CardContent>
            </Card>
        </Link>
    );
}
