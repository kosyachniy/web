'use client';

import { useTranslations } from 'next-intl';
import { PageHeader } from '@/shared/ui/page-header';
import { CatalogIcon, RefreshIcon } from '@/shared/ui/icons';
import { ProductsGrid } from '@/widgets/products-grid';
import { FiltersSidebar } from '@/widgets/filters-sidebar';

export default function CatalogPage() {
    const t = useTranslations('navigation');

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
                            {/* Search and Sort */}
                            <div className="flex flex-col sm:flex-row gap-4 mb-6">
                                <div className="flex-1">
                                    <input
                                        type="text"
                                        placeholder="Search products..."
                                        className="w-full px-4 py-2 border rounded-lg bg-background"
                                    />
                                </div>
                                <select className="px-4 py-2 border rounded-lg bg-background">
                                    <option>Sort by: Featured</option>
                                    <option>Price: Low to High</option>
                                    <option>Price: High to Low</option>
                                    <option>Newest First</option>
                                    <option>Best Rating</option>
                                </select>
                            </div>

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
