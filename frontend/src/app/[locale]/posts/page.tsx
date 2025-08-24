import { useTranslations } from 'next-intl';
import { Metadata } from 'next';

export const metadata: Metadata = {
    title: 'Posts - Categories & Content',
    description: 'Browse posts organized by categories',
};

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

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {/* Category Cards Placeholder */}
                        <div className="bg-card rounded-lg border p-6">
                            <h3 className="text-xl font-semibold mb-2">📚 Technology</h3>
                            <p className="text-muted-foreground mb-4">Latest tech news and tutorials</p>
                            <div className="text-sm text-muted-foreground">24 posts</div>
                        </div>

                        <div className="bg-card rounded-lg border p-6">
                            <h3 className="text-xl font-semibold mb-2">🎨 Design</h3>
                            <p className="text-muted-foreground mb-4">Creative design inspiration and tips</p>
                            <div className="text-sm text-muted-foreground">18 posts</div>
                        </div>

                        <div className="bg-card rounded-lg border p-6">
                            <h3 className="text-xl font-semibold mb-2">💼 Business</h3>
                            <p className="text-muted-foreground mb-4">Business insights and strategies</p>
                            <div className="text-sm text-muted-foreground">12 posts</div>
                        </div>

                        <div className="bg-card rounded-lg border p-6">
                            <h3 className="text-xl font-semibold mb-2">🔬 Science</h3>
                            <p className="text-muted-foreground mb-4">Scientific discoveries and research</p>
                            <div className="text-sm text-muted-foreground">9 posts</div>
                        </div>

                        <div className="bg-card rounded-lg border p-6">
                            <h3 className="text-xl font-semibold mb-2">🏃 Lifestyle</h3>
                            <p className="text-muted-foreground mb-4">Health, fitness, and life tips</p>
                            <div className="text-sm text-muted-foreground">15 posts</div>
                        </div>

                        <div className="bg-card rounded-lg border p-6">
                            <h3 className="text-xl font-semibold mb-2">🎯 Other</h3>
                            <p className="text-muted-foreground mb-4">Miscellaneous content and discussions</p>
                            <div className="text-sm text-muted-foreground">7 posts</div>
                        </div>
                    </div>

                    <div className="mt-12 text-center">
                        <div className="bg-muted rounded-lg p-8">
                            <h2 className="text-2xl font-semibold mb-4">Coming Soon</h2>
                            <p className="text-muted-foreground">
                                Advanced filtering, search functionality, and content management tools are currently in development.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}