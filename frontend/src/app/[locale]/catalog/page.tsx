import { useTranslations } from 'next-intl';
import { Metadata } from 'next';

export const metadata: Metadata = {
    title: 'Catalog - Products & Services',
    description: 'Browse our catalog of products and services with filters and search',
};

export default function CatalogPage() {
    const t = useTranslations('navigation');

    return (
        <div className="min-h-screen bg-background">
            <div className="container mx-auto px-4 py-8">
                <div className="max-w-7xl mx-auto">
                    <header className="mb-8">
                        <h1 className="text-4xl font-bold mb-4">
                            🛍️ {t('catalog')}
                        </h1>
                        <p className="text-lg text-muted-foreground">
                            Discover our curated collection of products and services with advanced filtering and search capabilities.
                        </p>
                    </header>

                    <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
                        {/* Filters Sidebar */}
                        <div className="lg:col-span-1">
                            <div className="bg-card rounded-lg border p-6 sticky top-4">
                                <h3 className="font-semibold mb-4">Filters</h3>
                                
                                {/* Categories */}
                                <div className="mb-6">
                                    <h4 className="font-medium mb-2">Categories</h4>
                                    <div className="space-y-2 text-sm">
                                        <label className="flex items-center">
                                            <input type="checkbox" className="mr-2" />
                                            Electronics (45)
                                        </label>
                                        <label className="flex items-center">
                                            <input type="checkbox" className="mr-2" />
                                            Clothing (32)
                                        </label>
                                        <label className="flex items-center">
                                            <input type="checkbox" className="mr-2" />
                                            Home & Garden (28)
                                        </label>
                                        <label className="flex items-center">
                                            <input type="checkbox" className="mr-2" />
                                            Books (19)
                                        </label>
                                        <label className="flex items-center">
                                            <input type="checkbox" className="mr-2" />
                                            Sports (15)
                                        </label>
                                    </div>
                                </div>

                                {/* Price Range */}
                                <div className="mb-6">
                                    <h4 className="font-medium mb-2">Price Range</h4>
                                    <div className="space-y-2 text-sm">
                                        <label className="flex items-center">
                                            <input type="radio" name="price" className="mr-2" />
                                            Under $25
                                        </label>
                                        <label className="flex items-center">
                                            <input type="radio" name="price" className="mr-2" />
                                            $25 - $50
                                        </label>
                                        <label className="flex items-center">
                                            <input type="radio" name="price" className="mr-2" />
                                            $50 - $100
                                        </label>
                                        <label className="flex items-center">
                                            <input type="radio" name="price" className="mr-2" />
                                            Over $100
                                        </label>
                                    </div>
                                </div>

                                {/* Rating */}
                                <div className="mb-6">
                                    <h4 className="font-medium mb-2">Rating</h4>
                                    <div className="space-y-2 text-sm">
                                        <label className="flex items-center">
                                            <input type="radio" name="rating" className="mr-2" />
                                            ⭐⭐⭐⭐⭐ (5 stars)
                                        </label>
                                        <label className="flex items-center">
                                            <input type="radio" name="rating" className="mr-2" />
                                            ⭐⭐⭐⭐ (4+ stars)
                                        </label>
                                        <label className="flex items-center">
                                            <input type="radio" name="rating" className="mr-2" />
                                            ⭐⭐⭐ (3+ stars)
                                        </label>
                                    </div>
                                </div>

                                <div className="bg-muted rounded p-3 text-sm text-muted-foreground">
                                    Advanced filters coming soon
                                </div>
                            </div>
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
                            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                                {/* Sample Product Cards */}
                                {[1, 2, 3, 4, 5, 6, 7, 8, 9].map((item) => (
                                    <div key={item} className="bg-card rounded-lg border overflow-hidden hover:shadow-lg transition-shadow">
                                        <div className="h-48 bg-muted flex items-center justify-center">
                                            <span className="text-4xl">📦</span>
                                        </div>
                                        <div className="p-4">
                                            <h3 className="font-semibold mb-2">Sample Product {item}</h3>
                                            <p className="text-muted-foreground text-sm mb-3">
                                                High-quality product with excellent features and great value for money.
                                            </p>
                                            <div className="flex items-center justify-between">
                                                <div>
                                                    <span className="text-lg font-bold">${(Math.random() * 100 + 20).toFixed(2)}</span>
                                                    <div className="flex items-center text-sm text-muted-foreground">
                                                        ⭐⭐⭐⭐⭐ (4.{Math.floor(Math.random() * 9)})
                                                    </div>
                                                </div>
                                                <button className="bg-primary text-primary-foreground px-3 py-1 rounded text-sm">
                                                    Add to Cart
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>

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

                    <div className="mt-12 text-center">
                        <div className="bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20 rounded-lg p-8">
                            <h2 className="text-2xl font-semibold mb-4">🔄 Coming Soon</h2>
                            <p className="text-muted-foreground mb-6">
                                Enhanced product catalog with real inventory management, advanced search algorithms, 
                                user reviews, and integrated payment processing.
                            </p>
                            <div className="flex justify-center space-x-4 text-sm">
                                <span className="bg-background px-3 py-1 rounded-full">Real-time Inventory</span>
                                <span className="bg-background px-3 py-1 rounded-full">AI-powered Search</span>
                                <span className="bg-background px-3 py-1 rounded-full">Payment Integration</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}