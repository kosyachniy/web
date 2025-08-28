'use client';

import Link from 'next/link';
import { Button } from '@/shared/ui/button';
import type { Category } from '@/entities/category';
import { getActiveSubcategories } from '@/entities/category';

interface SubcategoryNavigationProps {
  subcategories: Category[];
  className?: string;
}

export function SubcategoryNavigation({ 
  subcategories, 
  className = '' 
}: SubcategoryNavigationProps) {
  const activeSubcategories = getActiveSubcategories(subcategories);

  if (activeSubcategories.length === 0) {
    return null;
  }

  return (
    <div className={`flex flex-wrap gap-2 ${className}`}>
      {activeSubcategories.map(subcategory => {
        // If subcategory has a URL, render as clickable link
        if (subcategory.url && subcategory.url.trim().length > 0) {
          return (
            <Button
              key={subcategory.id}
              variant="outline"
              size="sm"
              asChild
              className="hover:bg-primary hover:text-white dark:hover:text-white transition-colors"
            >
              <Link href={`/posts/${subcategory.url}`}>
                {subcategory.title}
              </Link>
            </Button>
          );
        }
        
        // If no URL, render as non-clickable button
        return (
          <Button
            key={subcategory.id}
            variant="outline"
            size="sm"
            disabled
            className="opacity-60 cursor-not-allowed"
            title={`${subcategory.title} - No URL available`}
          >
            {subcategory.title}
          </Button>
        );
      })}
    </div>
  );
}