import type { Category } from '../model/category';

/**
 * Generate the canonical URL for a category
 */
export function getCategoryUrl(
  category: Category | null,
  locale?: string,
  baseUrl?: string
): string {
  const base = baseUrl || process.env.NEXT_PUBLIC_WEB || '';
  let canonical = base;

  // Add locale if different from default
  if (category?.locale && category.locale !== process.env.NEXT_PUBLIC_LOCALE) {
    canonical += `${category.locale}/`;
  } else if (locale && locale !== process.env.NEXT_PUBLIC_LOCALE) {
    canonical += `${locale}/`;
  }

  // Add category path
  if (category?.url) {
    canonical += `posts/${category.url}`;
  } else {
    canonical = canonical.slice(0, -1); // Remove trailing slash for root posts page
  }

  return canonical;
}

/**
 * Generate SEO title for a category page
 */
export function getCategoryTitle(category: Category | null, fallbackTitle: string, siteName?: string): string {
  const title = category ? category.title : fallbackTitle;
  const name = siteName || process.env.NEXT_PUBLIC_NAME || '';
  return `${title} | ${name}`;
}

/**
 * Build breadcrumb items from category hierarchy
 */
export function buildBreadcrumbs(category: Category | null, rootTitle: string) {
  const breadcrumbs = [
    {
      id: 0,
      title: rootTitle,
      url: '/posts',
      position: 0
    }
  ];

  if (category) {
    // Add parent categories
    if (category.parents) {
      category.parents.forEach((parent, index) => {
        breadcrumbs.push({
          id: parent.id,
          title: parent.title,
          url: `/posts/${parent.url}`,
          position: index + 1
        });
      });
    }

    // Add current category
    breadcrumbs.push({
      id: category.id,
      title: category.title,
      url: `/posts/${category.url}`,
      position: category.parents ? category.parents.length + 1 : 1
    });
  }

  return breadcrumbs;
}

/**
 * Generate structured data for category breadcrumbs
 */
export function generateBreadcrumbStructuredData(breadcrumbs: ReturnType<typeof buildBreadcrumbs>) {
  return {
    '@context': 'http://schema.org/',
    '@type': 'BreadcrumbList',
    itemListElement: breadcrumbs.map((item) => ({
      '@type': 'ListItem',
      position: item.position + 1,
      name: item.title,
      item: {
        '@type': 'Thing',
        '@id': item.url,
        name: item.title
      }
    }))
  };
}

/**
 * Generate structured data for category image
 */
export function generateCategoryImageStructuredData(category: Category) {
  if (!category.image) return null;

  return {
    '@context': 'http://schema.org/',
    '@type': 'ImageObject',
    contentUrl: category.image,
    name: category.title,
    description: category.description
  };
}

/**
 * Filter active subcategories (includes categories without URLs)
 * Note: API already filters by status=1, so we just return all subcategories
 */
export function getActiveSubcategories(subcategories: Category[]): Category[] {
  return subcategories;
}