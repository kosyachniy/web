import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { getTranslations } from 'next-intl/server';
import { PostsGrid } from '@/widgets/posts-list';
import { SubcategoryNavigation } from '@/widgets/category';
import { getCategoryByUrl, getSubcategories, getCategoryTitle, getCategoryUrl, buildBreadcrumbs, generateCategoryImageStructuredData, generateBreadcrumbStructuredData } from '@/entities/category';
import { PageHeader } from '@/shared/ui/page-header';
import { PostsIcon } from '@/shared/ui/icons';
import { BreadcrumbDescription } from '@/shared/ui/breadcrumb-description';
import Image from 'next/image';

interface CategoryPageProps {
  params: Promise<{
    locale: string;
    categoryUrl: string;
  }>;
  searchParams: Promise<{
    page?: string;
  }>;
}

export async function generateMetadata({ params }: CategoryPageProps): Promise<Metadata> {
  const { locale, categoryUrl } = await params;
  const category = await getCategoryByUrl(categoryUrl, locale);
  const t = await getTranslations('navigation');
  
  if (!category) {
    return {
      title: 'Category Not Found'
    };
  }

  const title = getCategoryTitle(category, t('posts'));
  const canonical = getCategoryUrl(category, locale);

  return {
    title,
    description: category.description || `Browse ${category.title} posts and articles`,
    openGraph: {
      title,
      description: category.description || `Browse ${category.title} posts and articles`,
      url: canonical,
      type: 'website',
      ...(category.image && { 
        images: [{
          url: category.image,
          width: 1200,
          height: 630,
          alt: category.title
        }]
      })
    },
    twitter: {
      card: 'summary_large_image',
      title,
      description: category.description || `Browse ${category.title} posts and articles`,
      ...(category.image && { images: [category.image] })
    },
    alternates: {
      canonical
    }
  };
}

export default async function CategoryPage({ params }: CategoryPageProps) {
  const { locale, categoryUrl } = await params;
  const t = await getTranslations('navigation');
  
  const category = await getCategoryByUrl(categoryUrl, locale);
  
  if (!category) {
    notFound();
  }

  const subcategories = await getSubcategories(category.id, locale);
  
  // Build breadcrumbs for navigation
  const breadcrumbs = buildBreadcrumbs(category, t('posts'));
  const imageStructuredData = generateCategoryImageStructuredData(category);
  const breadcrumbStructuredData = generateBreadcrumbStructuredData(breadcrumbs);

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          {/* Dynamic PageHeader with Breadcrumb Description */}
          <PageHeader
            icon={<PostsIcon size={24} />}
            iconClassName="bg-green-500/15 text-green-600 dark:bg-green-500/20 dark:text-green-400"
            title={category.title}
            description={<BreadcrumbDescription breadcrumbs={breadcrumbs} />}
          />

          {/* Subcategory Navigation */}
          {subcategories.length > 0 && (
            <SubcategoryNavigation 
              subcategories={subcategories}
              className="mb-6"
            />
          )}

          {/* Category Image (if exists) */}
          {category.image && (
            <div className="relative w-full h-48 md:h-64 rounded-[1rem] overflow-hidden mb-8">
              <Image
                src={category.image}
                alt={category.title}
                fill
                className="object-cover"
                priority
              />
            </div>
          )}

          {/* Category Description (if exists) */}
          {category.description && (
            <div className="mb-8">
              <p className="text-lg text-muted-foreground leading-relaxed">
                {category.description}
              </p>
            </div>
          )}

          {/* Category Content (HTML) */}
          {category.data && (
            <div className="mb-8">
              <div 
                className="prose prose-sm max-w-none dark:prose-invert"
                dangerouslySetInnerHTML={{ __html: category.data }}
              />
            </div>
          )}

          {/* Posts Grid */}
          <PostsGrid 
            categoryId={category.id}
            locale={locale}
          />

          {/* SEO Structured Data */}
          <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{
              __html: JSON.stringify(breadcrumbStructuredData)
            }}
          />
          
          {imageStructuredData && (
            <script
              type="application/ld+json"
              dangerouslySetInnerHTML={{
                __html: JSON.stringify(imageStructuredData)
              }}
            />
          )}
          
          <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{
              __html: JSON.stringify({
                '@context': 'http://schema.org/',
                '@type': 'CollectionPage',
                name: category.title,
                description: category.description,
                url: getCategoryUrl(category, locale),
                ...(category.image && { image: category.image }),
                mainEntity: {
                  '@type': 'ItemList',
                  name: `${category.title} Posts`,
                  description: `Collection of posts in ${category.title} category`
                }
              })
            }}
          />
        </div>
      </div>
    </div>
  );
}