import { Metadata } from 'next';
import { getTranslations } from 'next-intl/server';
import { PostsGrid } from '@/widgets/posts-list';
import { CategoryBreadcrumbs, SubcategoryNavigation } from '@/widgets/category';
import { getSubcategories, getCategoryTitle, getCategoryUrl } from '@/entities/category';
import { PageHeader } from '@/shared/ui/page-header';
import { PostsIcon } from '@/shared/ui/icons';

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
    const t = await getTranslations('navigation');
    
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

                    <PageHeader
                        icon={<PostsIcon size={24} />}
                        iconClassName="bg-green-500/15 text-green-600 dark:bg-green-500/20 dark:text-green-400"
                        title={t('posts')}
                        description="Browse and discover posts organized by categories. Find content that interests you most."
                    />

                    {/* Top-level Categories */}
                    {topCategories.length > 0 && (
                        <SubcategoryNavigation 
                            subcategories={topCategories}
                            className="mb-8"
                        />
                    )}

                    {/* All Posts */}
                    <PostsGrid locale={locale} />
                </div>
            </div>
        </div>
    );
}