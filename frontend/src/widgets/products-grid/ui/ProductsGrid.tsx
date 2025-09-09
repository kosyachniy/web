'use client';

import { ProductCard } from '@/widgets/product-card';
import { useToastActions } from '@/shared/hooks/useToast';
import { useAppSelector, useAppDispatch } from '@/shared/stores/store';
import { toggleCartItem, selectCartItemsAsSet } from '@/features/cart';
import { toggleFavorite, selectFavoriteItemsAsSet } from '@/features/favorites';

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

// Sample product data showcasing all card features
const sampleProducts = [
    {
        id: 1,
        title: 'Premium Wireless Headphones',
        description: 'High-quality wireless headphones with active noise cancellation and superior sound quality. Perfect for music lovers and professionals.',
        images: [
            'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400',
            'https://images.unsplash.com/photo-1484704849700-f032a568e944?w=400',
            'https://images.unsplash.com/photo-1524678606370-a47ad25cb82a?w=400'
        ],
        price: 199.99,
        originalPrice: 299.99,
        currency: '$',
        rating: 4.8,
        ratingCount: 234,
        category: 'Electronics',
        inStock: true,
        isNew: true,
        isFeatured: true,
        discount: 33
    },
    {
        id: 2,
        title: 'Smart Fitness Tracker',
        description: 'Advanced fitness tracker with heart rate monitoring, GPS tracking, and 7-day battery life.',
        images: [
            'https://images.unsplash.com/photo-1557935728-e6d1eaabe558?w=400',
            'https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=400'
        ],
        price: 149.99,
        currency: '$',
        rating: 4.5,
        ratingCount: 189,
        category: 'Sports',
        inStock: true,
        isFeatured: true
    },
    {
        id: 3,
        title: 'Organic Coffee Blend',
        description: 'Premium organic coffee beans sourced from sustainable farms. Rich, bold flavor with notes of chocolate and caramel.',
        images: [
            'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=400'
        ],
        price: 24.99,
        currency: '$',
        rating: 4.9,
        ratingCount: 156,
        category: 'Food & Beverage',
        inStock: true,
        isNew: true
    },
    {
        id: 4,
        title: 'Professional Camera Lens',
        description: 'High-performance 85mm f/1.4 lens perfect for portrait photography with beautiful bokeh and sharp focus.',
        images: [
            'https://images.unsplash.com/photo-1606983340126-99ab4feaa64a?w=400',
            'https://images.unsplash.com/photo-1481447709470-dfd6f0d2c802?w=400',
            'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400'
        ],
        price: 899.99,
        originalPrice: 1199.99,
        currency: '$',
        rating: 4.7,
        ratingCount: 89,
        category: 'Photography',
        inStock: true,
        discount: 25
    },
    {
        id: 5,
        title: 'Eco-Friendly Water Bottle',
        description: 'Sustainable stainless steel water bottle that keeps drinks cold for 24 hours or hot for 12 hours.',
        images: [
            'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400'
        ],
        price: 34.99,
        currency: '$',
        rating: 4.6,
        ratingCount: 267,
        category: 'Lifestyle',
        inStock: true,
        isNew: true
    },
    {
        id: 6,
        title: 'Gaming Mechanical Keyboard',
        description: 'RGB backlit mechanical keyboard with Cherry MX switches. Perfect for gaming and professional typing.',
        images: [
            'https://images.unsplash.com/photo-1541140532154-b024d705b90a?w=400',
            'https://images.unsplash.com/photo-1595044426077-d36d9236d54a?w=400'
        ],
        price: 129.99,
        originalPrice: 159.99,
        currency: '$',
        rating: 4.4,
        ratingCount: 145,
        category: 'Gaming',
        inStock: false,
        discount: 19
    },
    {
        id: 7,
        title: 'Luxury Skincare Set',
        description: 'Complete skincare routine with premium ingredients including vitamin C serum, retinol cream, and hyaluronic acid.',
        images: [
            'https://images.unsplash.com/photo-1556228578-dd6f2b34fa8a?w=400',
            'https://images.unsplash.com/photo-1570554886111-e80fcca6a029?w=400',
            'https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=400'
        ],
        price: 89.99,
        currency: '$',
        rating: 4.8,
        ratingCount: 203,
        category: 'Beauty',
        inStock: true,
        isFeatured: true
    },
    {
        id: 8,
        title: 'Smart Home Hub',
        description: 'Control all your smart devices from one central hub. Compatible with Alexa, Google Assistant, and Apple HomeKit.',
        images: [
            'https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=400'
        ],
        price: 79.99,
        originalPrice: 99.99,
        currency: '$',
        rating: 4.3,
        ratingCount: 178,
        category: 'Smart Home',
        inStock: true,
        discount: 20
    },
    {
        id: 9,
        title: 'Designer Sunglasses',
        description: 'Premium polarized sunglasses with UV400 protection and lightweight titanium frame. Perfect for any occasion.',
        images: [
            'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400',
            'https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=400'
        ],
        price: 249.99,
        currency: '$',
        rating: 4.7,
        ratingCount: 134,
        category: 'Fashion',
        inStock: true,
        isNew: true,
        isFeatured: true
    }
];

interface ProductsGridProps {
    // Props are optional now since we use Redux directly
    onProductAddToCart?: (productId: number) => void;
    onProductToggleFavorite?: (productId: number) => void;
    cartItems?: Set<number>;
    favoriteItems?: Set<number>;
}

export function ProductsGrid({ onProductAddToCart, onProductToggleFavorite, cartItems, favoriteItems }: ProductsGridProps) {
    const { success } = useToastActions();
    const dispatch = useAppDispatch();
    
    // Use Redux state if props are not provided
    const reduxCartItems = useAppSelector(selectCartItemsAsSet);
    const reduxFavoriteItems = useAppSelector(selectFavoriteItemsAsSet);
    
    const finalCartItems = cartItems || reduxCartItems;
    const finalFavoriteItems = favoriteItems || reduxFavoriteItems;

    const handleAddToCart = (product: Product) => {
        success(`${product.title} added to cart!`);
        console.log('Adding to cart:', product);
        
        // Use Redux action if no callback provided
        if (onProductAddToCart) {
            onProductAddToCart(product.id);
        } else {
            dispatch(toggleCartItem(product.id));
        }
    };

    const handleToggleFavorite = (product: Product) => {
        success(`${product.title} favorite status toggled!`);
        console.log('Toggle favorite:', product);
        
        // Use Redux action if no callback provided
        if (onProductToggleFavorite) {
            onProductToggleFavorite(product.id);
        } else {
            dispatch(toggleFavorite(product.id));
        }
    };

    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 items-start">
            {sampleProducts.map((product) => (
                <ProductCard
                    key={product.id}
                    product={product}
                    onAddToCart={handleAddToCart}
                    onToggleFavorite={handleToggleFavorite}
                    isInCart={finalCartItems.has(product.id)}
                    isInFavorites={finalFavoriteItems.has(product.id)}
                />
            ))}
        </div>
    );
}