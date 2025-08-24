'use client';

import { useTranslations } from 'next-intl';
import { PostsGrid } from '@/widgets/posts-list';

export default function PostsPage() {
    const t = useTranslations('navigation');

    return (
        <div className="min-h-screen bg-background">
            <div className="container mx-auto px-4 py-8">
                <div className="max-w-4xl mx-auto">
                    <header className="mb-8">
                        <h1 className="text-4xl font-bold mb-4">
                            📝 {t('posts')}
                        </h1>
                        <p className="text-lg text-muted-foreground">
                            Browse and discover posts organized by categories. Find content that interests you most.
                        </p>
                    </header>

                    <PostsGrid />
                </div>
            </div>
        </div>
    );
}