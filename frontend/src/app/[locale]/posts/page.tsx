import { Metadata } from 'next';
import { getTranslations } from 'next-intl/server';
import { PostsWithSearch } from '@/widgets/posts-list';
import { SubcategoryNavigation } from '@/widgets/category';
import { getSubcategories, getCategoryTitle, getCategoryUrl } from '@/entities/category';
import { PageHeader } from '@/shared/ui/page-header';
import { PostsIcon, PlusIcon } from '@/shared/ui/icons';
import { IconButton } from '@/shared/ui/icon-button';
import { ButtonGroup } from '@/shared/ui/button-group';

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
    twitter: {
      card: 'summary_large_image',
      title,
      description: 'Browse and discover posts organized by categories. Find content that interests you most.'
    },
    alternates: {
      canonical
    }
  };
}

export default async function PostsPage({ params }: PostsPageProps) {
    const { locale } = await params;
    const t = await getTranslations('navigation');
    const tPosts = await getTranslations('posts');
    
    // Get top-level categories (no parent)
    const topCategories = await getSubcategories(undefined, locale);

    return (
        <div className="min-h-screen bg-background">
            <div className="container mx-auto px-4 py-8">
                <div className="max-w-6xl mx-auto">
                    <PageHeader
                        icon={<PostsIcon size={24} />}
                        iconClassName="bg-green-500/15 text-green-600 dark:bg-green-500/20 dark:text-green-400"
                        title={t('posts')}
                        description="Browse and discover posts organized by categories. Find content that interests you most."
                        actions={
                            <ButtonGroup>
                                <IconButton 
                                    icon={<PlusIcon size={16} />} 
                                    variant="success" 
                                    responsive
                                >
                                    {tPosts('add')}
                                </IconButton>
                            </ButtonGroup>
                        }
                    />

                    {/* Top-level Categories */}
                    {topCategories.length > 0 && (
                        <SubcategoryNavigation 
                            subcategories={topCategories}
                            className="mb-8"
                        />
                    )}

                    {/* All Posts with Search */}
                    <PostsWithSearch locale={locale} />

                    {/* SEO Structured Data */}
                    <script
                        type="application/ld+json"
                        dangerouslySetInnerHTML={{
                            __html: JSON.stringify({
                                '@context': 'http://schema.org/',
                                '@type': 'CollectionPage',
                                name: t('posts'),
                                description: 'Browse and discover posts organized by categories. Find content that interests you most.',
                                url: getCategoryUrl(null, locale),
                                mainEntity: {
                                    '@type': 'ItemList',
                                    name: 'All Posts',
                                    description: 'Complete collection of posts across all categories'
                                }
                            })
                        }}
                    />
                </div>
            </div>
        </div>
    );
}