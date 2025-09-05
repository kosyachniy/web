'use client';

import { Box } from '@/shared/ui/box';
import { Post } from '@/entities/post';
import Image from 'next/image';
import Link from 'next/link';
import { EyeIcon } from '@/shared/ui/icons';
import { formatDate } from '@/shared/lib/date';

interface PostCardProps {
    post: Post;
}

export function PostCard({ post }: PostCardProps) {

    const stripHtml = (html: string) => {
        return html.replace(/<[^>]*>/g, '').substring(0, 150);
    };

    return (
        <Link href={`/posts/${post.url}`} className="block group">
            <Box className="h-full overflow-hidden hover:scale-[1.02] transition-all duration-200">
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

                <div className="p-4 pb-2">
                    <h3 className="text-lg font-semibold line-clamp-2 group-hover:text-primary transition-colors mb-2">
                        {post.title}
                    </h3>

                    {post.category_data && (
                        <div className="flex items-center gap-2 text-sm text-muted-foreground mb-4">
                            <span className="bg-primary/10 text-primary px-2 py-1 rounded-full text-xs">
                                {post.category_data.title}
                            </span>
                        </div>
                    )}
                </div>

                <div className="px-4 pb-4 pt-0">
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
                                <EyeIcon size={12} />
                                {post.views}
                            </span>
                        )}
                    </div>
                </div>
            </Box>
        </Link>
    );
}
