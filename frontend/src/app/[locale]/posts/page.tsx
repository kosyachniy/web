import { Metadata } from 'next';
import { getTranslations } from 'next-intl/server';
import { PostsGrid } from '@/widgets/posts-list';
import { CategoryBreadcrumbs, SubcategoryNavigation } from '@/widgets/category';
import { getSubcategories, getCategoryTitle, getCategoryUrl } from '@/entities/category';

interface PostsPageProps {
  params: Promise<{
    locale: string;
  }>;
  searchParams: Promise<{
    page?: string;
  }>;
}

export async function generateMetadata({ params }: PostsPageProps): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations('navigation');
  
  const title = getCategoryTitle(null, t('posts'));
  const canonical = getCategoryUrl(null, locale);

  return {
    title,
    description: 'Browse and discover posts organized by categories. Find content that interests you most.',
    openGraph: {
      title,
      description: 'Browse and discover posts organized by categories. Find content that interests you most.',
      url: canonical,
      type: 'website'
    },
    alternates: {
      canonical
    }
  };
}

export default async function PostsPage({ params }: PostsPageProps) {
    const { locale } = await params;
    
    // Get top-level categories (no parent)
    const topCategories = await getSubcategories(undefined, locale);

    return (
        <div className="min-h-screen bg-background">
            <div className="container mx-auto px-4 py-8">
                <div className="max-w-6xl mx-auto">
                    {/* Breadcrumbs */}
                    <CategoryBreadcrumbs 
                        category={null} 
                        className="mb-6"
                    />

                    <header className="mb-8">
                        <p className="text-lg text-muted-foreground">
                            Browse and discover posts organized by categories. Find content that interests you most.
                        </p>
                    </header>

                    {/* Top-level Categories */}
                    {topCategories.length > 0 && (
                        <div className="mb-8">
                            <h2 className="text-xl font-semibold mb-4">Categories</h2>
                            <SubcategoryNavigation 
                                subcategories={topCategories}
                                className="mb-6"
                            />
                        </div>
                    )}

                    {/* All Posts */}
                    <PostsGrid locale={locale} />
                </div>
            </div>
        </div>
    );
}