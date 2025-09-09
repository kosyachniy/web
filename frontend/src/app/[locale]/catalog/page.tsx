'use client';

import { useState, useCallback } from 'react';
import { useTranslations } from 'next-intl';
import { PageHeader } from '@/shared/ui/page-header';
import { CatalogIcon } from '@/shared/ui/icons';
import { ProductsGrid } from '@/widgets/products-grid';
import { FiltersSidebar } from '@/widgets/filters-sidebar';
import { Search, SearchFilters, SearchFilterConfig } from '@/shared/ui/search';

export default function CatalogPage() {
    const t = useTranslations('navigation');
    const tSearch = useTranslations('search');
    
    const [query, setQuery] = useState('');
    const [filters, setFilters] = useState<SearchFilters>({});

    // Configure inline filters (sort)
    const inlineFilters: SearchFilterConfig[] = [
        {
            type: 'sort',
            label: tSearch('sortBy'),
            key: 'sort',
            options: [
                { value: 'featured', label: tSearch('sortOptions.featured') },
                { value: 'priceAsc', label: tSearch('sortOptions.priceAsc') },
                { value: 'priceDesc', label: tSearch('sortOptions.priceDesc') },
                { value: 'newest', label: tSearch('sortOptions.newest') },
                { value: 'popular', label: tSearch('sortOptions.popular') }
            ]
        }
    ];

    // Configure popup filters (price range, promo code)
    const popupFilters: SearchFilterConfig[] = [
        {
            type: 'price-range',
            label: tSearch('priceRange'),
            key: 'priceRange'
        },
        {
            type: 'promo-code',
            label: tSearch('promoCode'),
            key: 'promoCode',
            placeholder: 'SAVE20, DISCOUNT10, etc.'
        }
    ];

    // Handle search
    const handleSearch = useCallback((searchQuery: string, searchFilters: SearchFilters) => {
        console.log('Catalog search:', { searchQuery, searchFilters });
        // TODO: Integrate with actual product search API
    }, []);

    return (
        <div className="min-h-screen bg-background">
            <div className="container mx-auto px-4 py-8">
                <div className="max-w-7xl mx-auto">
                    <PageHeader
                        icon={<CatalogIcon size={24} />}
                        iconClassName="bg-blue-500/15 text-blue-600 dark:bg-blue-500/20 dark:text-blue-400"
                        title={t('catalog')}
                        description="Discover our curated collection of products and services with advanced filtering and search capabilities."
                    />

                    <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
                        {/* Advanced Filters Sidebar */}
                        <div className="lg:col-span-1">
                            <FiltersSidebar className="sticky top-20" />
                        </div>

                        {/* Products Grid */}
                        <div className="lg:col-span-3">
                            {/* Advanced Search with Filters */}
                            <Search
                                value={query}
                                onChange={setQuery}
                                onSearch={handleSearch}
                                placeholder={tSearch('placeholder')}
                                filters={filters}
                                onFiltersChange={setFilters}
                                mode="inline-filters"
                                inlineFilters={inlineFilters}
                                popupFilters={popupFilters}
                                size="default"
                                className="mb-8"
                            />

                            {/* Products Grid */}
                            <ProductsGrid />

                            {/* Pagination */}
                            <div className="flex justify-center mt-8">
                                <div className="flex items-center space-x-2">
                                    <button className="px-3 py-1 border rounded">Previous</button>
                                    <button className="px-3 py-1 bg-primary text-primary-foreground rounded">1</button>
                                    <button className="px-3 py-1 border rounded">2</button>
                                    <button className="px-3 py-1 border rounded">3</button>
                                    <span className="px-3 py-1">...</span>
                                    <button className="px-3 py-1 border rounded">10</button>
                                    <button className="px-3 py-1 border rounded">Next</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
