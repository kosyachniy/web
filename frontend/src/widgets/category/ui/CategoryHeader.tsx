'use client';

import Image from 'next/image';
import type { Category } from '@/entities/category';
import { generateCategoryImageStructuredData } from '@/entities/category';

interface CategoryHeaderProps {
  category: Category;
  className?: string;
}

export function CategoryHeader({ category, className = '' }: CategoryHeaderProps) {
  const imageStructuredData = generateCategoryImageStructuredData(category);

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Category Image */}
      {category.image && (
        <div className="relative w-full h-48 md:h-64 rounded-lg overflow-hidden">
          <Image
            src={category.image}
            alt={category.title}
            fill
            className="object-cover"
            priority
          />
        </div>
      )}

      {/* Category Description */}
      {category.description && (
        <p className="text-lg text-muted-foreground leading-relaxed">
          {category.description}
        </p>
      )}

      {/* Category Content (HTML) */}
      {category.data && (
        <div 
          className="prose prose-sm max-w-none dark:prose-invert"
          dangerouslySetInnerHTML={{ __html: category.data }}
        />
      )}

      {/* Structured Data for Category Image */}
      {imageStructuredData && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify(imageStructuredData)
          }}
        />
      )}
    </div>
  );
}