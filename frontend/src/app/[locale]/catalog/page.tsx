'use client';

import { useState, useCallback } from 'react';
import { useTranslations } from 'next-intl';
import { PageHeader } from '@/shared/ui/page-header';
import { ButtonGroup } from '@/shared/ui/button-group';
import { IconButton } from '@/shared/ui/icon-button';
import { Badge } from '@/shared/ui/badge';
import { CatalogIcon, HeartIcon, ShoppingIcon } from '@/shared/ui/icons';
import { ProductsGrid } from '@/widgets/products-grid';
import { FiltersSidebar } from '@/widgets/filters-sidebar';
import { Search, SearchFilters, SearchFilterConfig } from '@/shared/ui/search';
import { useAppSelector, useAppDispatch } from '@/shared/stores/store';
import { toggleCartItem, selectCartItemsAsSet } from '@/features/cart';
import { toggleFavorite, selectFavoriteItemsAsSet } from '@/features/favorites';

export default function CatalogPage() {
    const t = useTranslations('navigation');
    const tCatalog = useTranslations('catalog.product');
    const tSearch = useTranslations('search');

    const [query, setQuery] = useState('');
    const [filters, setFilters] = useState<SearchFilters>({});
    
    // Redux state
    const dispatch = useAppDispatch();
    const cartItems = useAppSelector(selectCartItemsAsSet);
    const favoriteItems = useAppSelector(selectFavoriteItemsAsSet);

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

    // Handle favorites and cart actions
    const handleOpenFavorites = () => {
        console.log('Opening favorites panel with', favoriteItems.size, 'items');
        // TODO: Open favorites modal/panel
    };

    const handleOpenCart = () => {
        console.log('Opening cart panel with', cartItems.size, 'items');
        // TODO: Open cart modal/panel
    };

    // Handle product interactions from ProductsGrid
    const handleProductAddToCart = (productId: number) => {
        dispatch(toggleCartItem(productId));
    };

    const handleProductToggleFavorite = (productId: number) => {
        dispatch(toggleFavorite(productId));
    };

    return (
        <div className="min-h-screen bg-background">
            <div className="container mx-auto px-4 py-8">
                <div className="max-w-7xl mx-auto">
                    <PageHeader
                        icon={<CatalogIcon size={24} />}
                        iconClassName="bg-blue-500/15 text-blue-600 dark:bg-blue-500/20 dark:text-blue-400"
                        title={t('catalog')}
                        description="Discover our curated collection of products and services with advanced filtering and search capabilities."
                        actions={
                            <ButtonGroup>
                                <IconButton
                                    variant="outline"
                                    icon={<HeartIcon size={16} />}
                                    onClick={handleOpenFavorites}
                                    responsive
                                    className="relative"
                                >
                                    {tCatalog('favorite')}
                                    {favoriteItems.size > 0 && (
                                        <Badge
                                            variant="destructive"
                                            className="absolute -top-1 -right-1 min-w-[1rem] h-4 flex items-center justify-center p-0 text-[10px] text-white bg-red-500 border-red-500 pointer-events-none z-10"
                                        >
                                            {favoriteItems.size}
                                        </Badge>
                                    )}
                                </IconButton>

                                <IconButton
                                    variant="outline"
                                    icon={<ShoppingIcon size={16} />}
                                    onClick={handleOpenCart}
                                    responsive
                                    className="relative"
                                >
                                    {tCatalog('cart')}
                                    {cartItems.size > 0 && (
                                        <Badge
                                            variant="destructive"
                                            className="absolute -top-1 -right-1 min-w-[1rem] h-4 flex items-center justify-center p-0 text-[10px] text-white bg-red-500 border-red-500 pointer-events-none z-10"
                                        >
                                            {cartItems.size}
                                        </Badge>
                                    )}
                                </IconButton>
                            </ButtonGroup>
                        }
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
                            <ProductsGrid
                                onProductAddToCart={handleProductAddToCart}
                                onProductToggleFavorite={handleProductToggleFavorite}
                                cartItems={cartItems}
                                favoriteItems={favoriteItems}
                            />

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
