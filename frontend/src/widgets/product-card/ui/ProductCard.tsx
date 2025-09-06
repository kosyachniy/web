'use client';

import { Card } from '@/shared/ui/card';
import { Button } from '@/shared/ui/button';
import { ShoppingIcon, TagIcon, TrendingIcon, StarIcon, ReviewsIcon } from '@/shared/ui/icons';

interface Product {
    id: number;
    title: string;
    description: string;
    images: string[];
    price: number;
    originalPrice?: number;
    currency?: string;
    rating?: number;
    ratingCount?: number;
    category?: string;
    inStock?: boolean;
    isNew?: boolean;
    isFeatured?: boolean;
    discount?: number;
}

interface ProductCardProps {
    product: Product;
    onAddToCart?: (product: Product) => void;
}

export function ProductCard({ product, onAddToCart }: ProductCardProps) {
    // Prepare filters (category, rating and reviews in filters row)
    const filters = [];
    
    // Add category to filters if available
    if (product.category) {
        filters.push({
            icon: <TagIcon size={12} />,
            value: product.category
        });
    }
    
    if (product.rating) {
        filters.push({
            icon: <StarIcon size={12} />,
            value: product.rating
        });
    }
    
    if (product.ratingCount) {
        filters.push({
            icon: <ReviewsIcon size={12} />,
            value: product.ratingCount
        });
    }

    // Prepare tags (below description)
    const tags = [];
    
    if (product.isNew) {
        tags.push({
            icon: <TagIcon size={10} />,
            label: 'New',
            variant: 'success' as const
        });
    }
    
    if (product.isFeatured) {
        tags.push({
            icon: <TrendingIcon size={10} />,
            label: 'Featured',
            variant: 'warning' as const
        });
    }
    
    if (!product.inStock) {
        tags.push({
            label: 'Out of Stock',
            variant: 'destructive' as const
        });
    }

    // Prepare actions - single button only
    const actions = onAddToCart ? (
        <Button
            variant={product.inStock ? "default" : "outline"}
            size="sm"
            disabled={!product.inStock}
            onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                onAddToCart(product);
            }}
            className="w-full"
        >
            <ShoppingIcon size={12} />
            {product.inStock ? 'Add to Cart' : 'Unavailable'}
        </Button>
    ) : null;

    return (
        <Card
            title={product.title}
            description={product.description}
            images={product.images}
            filters={filters}
            tags={tags}
            price={product.price}
            originalPrice={product.originalPrice}
            currency={product.currency}
            actions={actions}
            variant="product"
            onClick={() => {
                // Handle product click - could navigate to product detail page
                console.log('Product clicked:', product.title);
            }}
        />
    );
}