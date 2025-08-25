import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { getTranslations } from 'next-intl/server';
import { PostsGrid } from '@/widgets/posts-list';
import { CategoryBreadcrumbs, CategoryHeader, SubcategoryNavigation } from '@/widgets/category';
import { getCategoryByUrl, getSubcategories, getCategoryTitle, getCategoryUrl } from '@/entities/category';

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
    description: category.description,
    openGraph: {
      title,
      description: category.description,
      url: canonical,
      type: 'website',
      ...(category.image && { images: [category.image] })
    },
    alternates: {
      canonical
    }
  };
}

export default async function CategoryPage({ params }: CategoryPageProps) {
  const { locale, categoryUrl } = await params;
  
  const category = await getCategoryByUrl(categoryUrl, locale);
  
  if (!category) {
    notFound();
  }

  const subcategories = await getSubcategories(category.id, locale);

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          {/* Breadcrumbs and Category Title */}
          <CategoryBreadcrumbs 
            category={category} 
            className="mb-6"
          />

          {/* Subcategory Navigation */}
          {subcategories.length > 0 && (
            <SubcategoryNavigation 
              subcategories={subcategories}
              className="mb-6"
            />
          )}

          {/* Category Header (image, description, content) */}
          <CategoryHeader 
            category={category}
            className="mb-8"
          />

          {/* Posts Grid */}
          <PostsGrid 
            categoryId={category.id}
            locale={locale}
          />
        </div>
      </div>
    </div>
  );
}