'use client';

import * as React from 'react';
import { useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { cva, type VariantProps } from 'class-variance-authority';

import { cn } from '@/shared/lib/utils';
import { ChevronRightIcon, HeartIcon } from './icons';

// Card variants for different use cases
const cardVariants = cva(
  'group cursor-pointer block card-hover shadow-box rounded-[1rem] overflow-hidden',
  {
    variants: {
      variant: {
        default: 'hover:shadow-lg transition-shadow',
        minimal: 'shadow-sm hover:shadow-md transition-shadow',
        product: 'hover:shadow-xl transition-shadow',
      },
      size: {
        sm: 'max-w-sm',
        default: 'w-full',
        lg: 'max-w-lg',
      }
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

// Image slider component
interface ImageSliderProps {
  images: string[];
  alt: string;
  className?: string;
  showDiscount?: boolean;
  discountPercent?: number;
  showLikeButton?: boolean;
  isLiked?: boolean;
  onLikeClick?: (e: React.MouseEvent) => void;
}

function ImageSlider({ images, alt, className, showDiscount, discountPercent, showLikeButton, isLiked, onLikeClick }: ImageSliderProps) {
  const [currentImage, setCurrentImage] = useState(0);
  const hasMultipleImages = images.length > 1;

  const nextImage = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setCurrentImage((prev) => (prev + 1) % images.length);
  };

  const prevImage = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setCurrentImage((prev) => (prev - 1 + images.length) % images.length);
  };

  return (
    <div className={cn('relative w-full h-48 overflow-hidden', className)}>
      <Image
        src={images[currentImage]}
        alt={alt}
        fill
        className="object-cover"
        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
      />

      {/* Discount Badge */}
      {showDiscount && discountPercent && (
        <div className="absolute bottom-2 left-2 bg-black text-white text-xs font-semibold px-2 py-1 rounded-[0.75rem] shadow-sm">
          -{discountPercent}%
        </div>
      )}

      {/* Like Button */}
      {showLikeButton && onLikeClick && (
        <button
          onClick={onLikeClick}
          className={cn(
            'absolute top-2 right-2 w-8 h-8 rounded-full flex items-center justify-center transition-all shadow-sm cursor-pointer',
            'opacity-80 hover:opacity-100 hover:scale-110',
            isLiked
              ? 'bg-red-500 text-white'
              : 'bg-white/80 text-gray-600 hover:bg-white'
          )}
        >
          <HeartIcon
            size={16}
            className={cn(
              'transition-all',
              isLiked && 'scale-110'
            )}
          />
        </button>
      )}

      {/* Image Navigation */}
      {hasMultipleImages && (
        <>
          {/* Navigation Dots */}
          <div className="absolute bottom-2 left-1/2 transform -translate-x-1/2 flex gap-1">
            {images.map((_, index) => (
              <button
                key={index}
                onClick={(e) => {
                  e.preventDefault();
                  e.stopPropagation();
                  setCurrentImage(index);
                }}
                className={cn(
                  'w-2 h-2 rounded-full transition-all cursor-pointer',
                  index === currentImage
                    ? 'bg-white shadow-md'
                    : 'bg-white/50 hover:bg-white/75'
                )}
              />
            ))}
          </div>

          {/* Navigation Arrows */}
          <button
            onClick={prevImage}
            className="absolute left-2 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white w-8 h-8 rounded-full flex items-center justify-center transition-all opacity-0 group-hover:opacity-100 cursor-pointer"
          >
            <ChevronRightIcon size={12} className="rotate-180" />
          </button>
          <button
            onClick={nextImage}
            className="absolute right-2 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white w-8 h-8 rounded-full flex items-center justify-center transition-all opacity-0 group-hover:opacity-100 cursor-pointer"
          >
            <ChevronRightIcon size={12} />
          </button>
        </>
      )}
    </div>
  );
}

// Filter/Info Badge component
interface InfoBadgeProps {
  icon?: React.ReactNode;
  label: string;
  count?: number;
  variant?: 'default' | 'primary' | 'success' | 'warning' | 'destructive';
}

function InfoBadge({ icon, label, count, variant = 'default' }: InfoBadgeProps) {
  const variants = {
    default: 'bg-muted text-muted-foreground',
    primary: 'bg-primary/10 text-primary',
    success: 'bg-green-500/10 text-green-600 dark:text-green-400',
    warning: 'bg-orange-500/10 text-orange-600 dark:text-orange-400',
    destructive: 'bg-destructive/10 text-destructive',
  };

  return (
    <span className={cn('inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium', variants[variant])}>
      {icon}
      {label}
      {typeof count === 'number' && <span className="font-semibold">({count})</span>}
    </span>
  );
}

// Pricing component
interface PricingProps {
  price: number;
  originalPrice?: number;
  currency?: string;
  className?: string;
}

function Pricing({ price, originalPrice, currency = '$', className }: PricingProps) {
  const hasDiscount = originalPrice && originalPrice > price;

  return (
    <div className={cn('flex items-center gap-2', className)}>
      <span className="text-lg font-bold">
        {currency}{price.toFixed(2)}
      </span>
      {hasDiscount && (
        <span className="text-sm text-muted-foreground line-through">
          {currency}{originalPrice.toFixed(2)}
        </span>
      )}
    </div>
  );
}

// Filter item interface (plain icon + value)
interface FilterItem {
  icon?: React.ReactNode;
  value: string | number;
}

// Main Card component props
interface CardProps extends VariantProps<typeof cardVariants> {
  // Basic content
  title: string;
  description?: string;
  images: string[];

  // Navigation
  href?: string;
  onClick?: () => void;

  // Filters above title (plain icon + value)
  filters?: FilterItem[];

  // Tags below description
  tags?: InfoBadgeProps[];

  // Pricing (for products)
  price?: number;
  originalPrice?: number;
  currency?: string;

  // Metadata (author, date, views, etc.)
  metadata?: Array<{
    icon?: React.ReactNode;
    label: string;
    value: string | number;
  }>;

  // Actions (for products - add to cart, etc.)
  actions?: React.ReactNode;

  // Like functionality
  showLikeButton?: boolean;
  isLiked?: boolean;
  onLikeClick?: (id?: string | number) => void;
  id?: string | number;

  // Additional props
  className?: string;
  children?: React.ReactNode;
}

function Card({
  title,
  description,
  images,
  href,
  onClick,
  filters = [],
  tags = [],
  price,
  originalPrice,
  currency = '$',
  metadata = [],
  actions,
  showLikeButton = false,
  isLiked = false,
  onLikeClick,
  id,
  variant,
  size,
  className,
  children,
  ...props
}: CardProps) {
  const hasImages = images.length > 0;
  const hasPricing = typeof price === 'number';
  const discountPercent = originalPrice && price ? Math.round(((originalPrice - price) / originalPrice) * 100) : undefined;

  const handleLikeClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (onLikeClick) {
      onLikeClick(id);
    }
  };

  const CardContent = () => (
    <div className={cn('bg-card text-card-foreground', className)} {...props}>
      {/* Image Section */}
      {hasImages && (
        <ImageSlider
          images={images}
          alt={title}
          showDiscount={hasPricing && !!discountPercent}
          discountPercent={discountPercent}
          showLikeButton={showLikeButton}
          isLiked={isLiked}
          onLikeClick={handleLikeClick}
        />
      )}

      <div className="p-3">
        {/* Filters Row */}
        {filters.length > 0 && (
          <div className="flex items-center gap-3 text-xs text-muted-foreground mb-2">
            {filters.map((filter, index) => (
              <span key={index} className="flex items-center gap-1">
                {filter.icon}
                {filter.value}
              </span>
            ))}
          </div>
        )}

        {/* Title */}
        <h3 className="text-lg font-semibold line-clamp-2 group-hover:text-primary transition-colors">
          {title}
        </h3>

        {/* Description */}
        {description && (
          <p className="text-sm text-muted-foreground line-clamp-3">
            {description}
          </p>
        )}

        {/* Tags Row (below description) */}
        {tags.length > 0 && (
          <div className="flex items-center gap-2 mt-2 flex-wrap">
            {tags.map((tag, index) => (
              <InfoBadge key={index} {...tag} />
            ))}
          </div>
        )}

        {/* Pricing */}
        {hasPricing && (
          <div className="mt-2">
            <Pricing
              price={price}
              originalPrice={originalPrice}
              currency={currency}
            />
          </div>
        )}

        {/* Custom Content */}
        {children && <div className="mt-2">{children}</div>}

        {/* Metadata */}
        {metadata.length > 0 && (
          <div className="flex items-center gap-4 text-xs text-muted-foreground mt-2">
            {metadata.map((item, index) => (
              <span key={index} className="flex items-center gap-1">
                {item.icon}
                {item.value}
              </span>
            ))}
          </div>
        )}

        {/* Actions */}
        {actions && (
          <div className="flex items-center justify-end gap-2 mt-3">
            {actions}
          </div>
        )}
      </div>
    </div>
  );

  // Wrap with Link if href provided
  if (href) {
    return (
      <Link href={href} className={cn(cardVariants({ variant, size }))}>
        <CardContent />
      </Link>
    );
  }

  // Wrap with button-like div if onClick provided
  if (onClick) {
    return (
      <div
        onClick={onClick}
        className={cn(cardVariants({ variant, size }))}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            onClick();
          }
        }}
      >
        <CardContent />
      </div>
    );
  }

  // Static card
  return (
    <div className={cn(cardVariants({ variant, size }), 'cursor-default')}>
      <CardContent />
    </div>
  );
}

// Export components
export { Card, ImageSlider, InfoBadge, Pricing };
export type { CardProps, FilterItem, ImageSliderProps, InfoBadgeProps, PricingProps };
