'use client';

import React, { useState, useCallback } from 'react';
import { Input } from './input';
import { Button } from './button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './select';
import { Popover, PopoverContent, PopoverTrigger } from './popover';
import { cn } from '@/shared/lib/utils';
import { SearchIcon, FilterIcon, CloseIcon, MenuIcon, StarIcon, ArrowUpIcon, ArrowDownIcon, ClockIcon, TrendingIcon } from './icons';
import { useTranslations } from 'next-intl';

// Helper function to get sort option icons
function getSortIcon(sortValue: string) {
  switch (sortValue) {
    case 'featured':
      return <StarIcon size={12} className="text-amber-500" />;
    case 'priceAsc':
      return <ArrowUpIcon size={12} className="text-green-500" />;
    case 'priceDesc':
      return <ArrowDownIcon size={12} className="text-red-500" />;
    case 'newest':
      return <ClockIcon size={12} className="text-blue-500" />;
    case 'popular':
      return <TrendingIcon size={12} className="text-orange-500" />;
    default:
      return <StarIcon size={12} className="text-muted-foreground" />;
  }
}

// Helper function to format filter labels for display
function getFilterLabel(key: string, value: string | number | boolean | SearchPriceRange | null | undefined, t: (key: string) => string): string {
  switch (key) {
    case 'sort':
      return `${t('sortBy')}: ${t(`sortOptions.${value}`)}`;
    case 'priceRange':
      if (value && typeof value === 'object' && 'min' in value) {
        const priceRange = value as SearchPriceRange;
        if (priceRange.min && priceRange.max) {
          return `${t('priceRange')}: ${priceRange.min} - ${priceRange.max}`;
        } else if (priceRange.min) {
          return `${t('priceFrom')}: ${priceRange.min}`;
        } else if (priceRange.max) {
          return `${t('priceTo')}: ${priceRange.max}`;
        }
      }
      return `${t('priceRange')}: ${value}`;
    case 'promoCode':
      return `${t('promoCode')}: ${value}`;
    case 'category':
      return `${t('category')}: ${value}`;
    default:
      return `${key}: ${value}`;
  }
}

// Types for flexible filter system
export interface SearchSortOption {
  value: string;
  label: string;
}

export interface SearchPriceRange {
  min: number | null;
  max: number | null;
}

export interface SearchFilters {
  sort?: string;
  priceRange?: SearchPriceRange;
  promoCode?: string;
  category?: string;
  [key: string]: string | number | boolean | SearchPriceRange | null | undefined; // Allow custom filters
}

export interface SearchFilterConfig {
  type: 'sort' | 'price-range' | 'promo-code' | 'category' | 'custom';
  label: string;
  key: string;
  options?: SearchSortOption[]; // For sort and category filters
  placeholder?: string; // For text inputs
  component?: React.ComponentType<{
    value: string | number | boolean | SearchPriceRange | null | undefined;
    onChange: (value: string | number | boolean | SearchPriceRange | null | undefined) => void;
    onClear: () => void;
  }>; // For custom filters
}

export interface SearchProps {
  // Search functionality
  value?: string;
  onChange?: (value: string) => void;
  onSearch?: (query: string, filters: SearchFilters) => void;
  placeholder?: string;
  
  // Filter configuration
  filters?: SearchFilters;
  onFiltersChange?: (filters: SearchFilters) => void;
  
  // Display modes
  mode?: 'simple' | 'inline-filters' | 'popup-filters';
  inlineFilters?: SearchFilterConfig[];
  popupFilters?: SearchFilterConfig[];
  
  // Styling
  className?: string;
  size?: 'sm' | 'default' | 'lg';
  
  // Optional search button
  showSearchButton?: boolean;
  
  // Loading state
  loading?: boolean;
  
  // Accessibility
  'aria-label'?: string;
}

// Main Search Component
export function Search({
  value = '',
  onChange,
  onSearch,
  placeholder,
  filters = {},
  onFiltersChange,
  mode = 'simple',
  inlineFilters = [],
  popupFilters = [],
  className,
  size = 'default',
  showSearchButton = false,
  loading = false,
  'aria-label': ariaLabel,
}: SearchProps) {
  const t = useTranslations('search');
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const [localQuery, setLocalQuery] = useState(value);
  
  // Size variants for exact fixed height (not minimum)
  const sizeClasses = {
    sm: 'py-2 px-2 h-[2.5rem]',    // 40px exact height
    default: 'py-2 px-3 h-[3.5rem]', // 56px exact height (inline search)
    lg: 'py-3 px-4 h-[4rem]'       // 64px exact height
  };


  const handleQueryChange = useCallback((newQuery: string) => {
    setLocalQuery(newQuery);
    onChange?.(newQuery);
  }, [onChange]);

  const handleSearch = useCallback((searchQuery?: string, searchFilters?: SearchFilters) => {
    onSearch?.(searchQuery ?? localQuery, searchFilters ?? filters);
  }, [localQuery, filters, onSearch]);

  const handleKeyPress = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  }, [handleSearch]);

  const handleFilterChange = useCallback((key: string, value: string | number | boolean | SearchPriceRange | null | undefined) => {
    const newFilters = { ...filters, [key]: value };
    onFiltersChange?.(newFilters);
    // Immediate search on filter change
    handleSearch(localQuery, newFilters);
  }, [filters, onFiltersChange, handleSearch, localQuery]);

  const clearFilter = useCallback((key: string) => {
    const newFilters = { ...filters };
    delete newFilters[key];
    onFiltersChange?.(newFilters);
    // Immediate search on filter clear
    handleSearch(localQuery, newFilters);
  }, [filters, onFiltersChange, handleSearch, localQuery]);

  const hasActiveFilters = Object.keys(filters).length > 0;

  return (
    <div className={cn('space-y-4', className)}>
      {/* Unified Input Group */}
      <div 
        className={cn(
          // Unified container with 1rem border-radius, no borders
          'bg-background rounded-[1rem]',
          // Card-style shadow and hover effects
          'shadow-[0_0.25rem_1.5rem_rgba(0,0,0,0.12)]',
          'transition-all duration-300 ease-[cubic-bezier(0,0,0.5,1)]',
          'hover:scale-[1.01]',
          'flex items-center overflow-hidden', // Remove individual borders between elements
          sizeClasses[size]
        )}
        role="search"
        aria-label={ariaLabel || t('searchArea')}
      >
        {/* Main search input - full height, no search icon */}
        <div className="flex-1 relative h-full">
          <Input
            type="text"
            value={localQuery}
            onChange={(e) => handleQueryChange(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={placeholder || t('placeholder')}
            className={cn(
              'border-0 bg-transparent shadow-none pl-4 pr-10 focus:ring-0 focus:ring-offset-0 rounded-none h-full',
              'focus:outline-none focus:ring-0'
            )}
            disabled={loading}
            aria-label={t('searchInput')}
          />
          {localQuery && (
            <button
              type="button"
              onClick={() => handleQueryChange('')}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors cursor-pointer"
              aria-label={t('clearSearch')}
            >
              <CloseIcon size={14} />
            </button>
          )}
        </div>

        {/* Inline filters - integrated in the same container */}
        {mode === 'inline-filters' && inlineFilters.length > 0 && (
          <>
            {inlineFilters.map((filterConfig) => (
              <div key={filterConfig.key} className="h-full border-l border-border">
                <FilterComponent
                  config={filterConfig}
                  value={filters[filterConfig.key]}
                  onChange={(value) => handleFilterChange(filterConfig.key, value)}
                  onClear={() => clearFilter(filterConfig.key)}
                  integrated={true} // Tells component it's part of unified group
                />
              </div>
            ))}
          </>
        )}

        {/* Popup filters trigger */}
        {mode === 'popup-filters' && popupFilters.length > 0 && (
          <div className="h-full border-l border-border">
            <Popover open={isPopupOpen} onOpenChange={setIsPopupOpen}>
              <PopoverTrigger asChild>
                <Button
                  variant="ghost"
                  className={cn(
                    'border-0 bg-transparent shadow-none rounded-none px-3 h-full cursor-pointer',
                    'hover:bg-muted/50 transition-colors',
                    hasActiveFilters && 'text-primary',
                    'relative'
                  )}
                  aria-label={t('openFilters')}
                >
                  <FilterIcon size={16} />
                  <span className="hidden sm:inline-block ml-2">{t('filters')}</span>
                  {hasActiveFilters && (
                    <span className="absolute -top-1 -right-1 w-2 h-2 bg-primary rounded-full"></span>
                  )}
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-80 p-4" align="end">
                <FilterPopup
                  filters={popupFilters}
                  values={filters}
                  onChange={handleFilterChange}
                  onClear={clearFilter}
                  onClose={() => setIsPopupOpen(false)}
                />
              </PopoverContent>
            </Popover>
          </div>
        )}

        {/* Advanced filters button (ellipsis) for inline + popup mode */}
        {mode === 'inline-filters' && popupFilters.length > 0 && (
          <div className="h-full border-l border-border">
            <Popover open={isPopupOpen} onOpenChange={setIsPopupOpen}>
              <PopoverTrigger asChild>
                <Button
                  variant="ghost"
                  className={cn(
                    'border-0 bg-transparent shadow-none rounded-none px-3 h-full cursor-pointer',
                    'hover:bg-muted/50 transition-colors',
                    hasActiveFilters && 'text-primary'
                  )}
                  aria-label={t('moreFilters')}
                >
                  <MenuIcon size={16} />
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-80 p-4" align="end">
                <FilterPopup
                  filters={popupFilters}
                  values={filters}
                  onChange={handleFilterChange}
                  onClear={clearFilter}
                  onClose={() => setIsPopupOpen(false)}
                />
              </PopoverContent>
            </Popover>
          </div>
        )}

        {/* Optional Search button */}
        {showSearchButton && (
          <div className="h-full border-l border-border">
            <Button
              onClick={() => handleSearch()}
              disabled={loading}
              className={cn(
                'border-0 shadow-none rounded-none px-4 h-full cursor-pointer',
                'hover:bg-primary/10 transition-colors'
              )}
              aria-label={t('searchButton')}
            >
              <SearchIcon size={16} className="mr-2" />
              <span className="hidden sm:inline-block">{t('search')}</span>
            </Button>
          </div>
        )}
      </div>

      {/* Active filters display */}
      {hasActiveFilters && (
        <div className="flex items-center gap-2">
          <span className="text-sm text-muted-foreground">{t('activeFilters')}:</span>
          <div className="flex flex-wrap gap-2">
            {Object.entries(filters).map(([key, value]) => (
              value && (
                <FilterChip
                  key={key}
                  label={getFilterLabel(key, value, t)}
                  onRemove={() => clearFilter(key)}
                />
              )
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// Individual filter component with integrated styling option
function FilterComponent({ 
  config, 
  value, 
  onChange, 
  onClear,
  integrated = false
}: {
  config: SearchFilterConfig;
  value: string | number | boolean | SearchPriceRange | null | undefined;
  onChange: (value: string | number | boolean | SearchPriceRange | null | undefined) => void;
  onClear: () => void;
  integrated?: boolean;
}) {
  const t = useTranslations('search');

  const integratedClasses = integrated 
    ? 'border-0 bg-transparent shadow-none rounded-none focus:ring-0 focus:ring-offset-0 cursor-pointer hover:bg-muted/30 transition-colors h-full'
    : 'cursor-pointer hover:bg-muted/30 transition-colors h-full';

  switch (config.type) {
    case 'sort':
      return (
        <Select value={String(value || '')} onValueChange={onChange}>
          <SelectTrigger className={cn(
            'w-48',
            integratedClasses
          )}>
            <SelectValue placeholder={config.label} />
          </SelectTrigger>
          <SelectContent>
            {config.options?.map((option) => (
              <SelectItem key={option.value} value={option.value} className="cursor-pointer pl-3">
                <div className="flex items-center gap-2">
                  {getSortIcon(option.value)}
                  <span>{option.label}</span>
                </div>
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      );
      
    case 'category':
      return (
        <Select value={String(value || '')} onValueChange={onChange}>
          <SelectTrigger className={cn(
            'w-40',
            integratedClasses
          )}>
            <SelectValue placeholder={config.label} />
          </SelectTrigger>
          <SelectContent>
            {config.options?.map((option) => (
              <SelectItem key={option.value} value={option.value} className="cursor-pointer pl-3">
                <div className="flex items-center">
                  <span>{option.label}</span>
                </div>
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      );
      
    case 'promo-code':
      return (
        <div className="relative w-32 h-full">
          <Input
            type="text"
            value={String(value || '')}
            onChange={(e) => onChange(e.target.value)}
            placeholder={config.placeholder || t('promoCode')}
            className={cn(
              integratedClasses
            )}
          />
          {value && (
            <button
              type="button"
              onClick={onClear}
              className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground cursor-pointer"
            >
              <CloseIcon size={12} />
            </button>
          )}
        </div>
      );
      
    case 'custom':
      if (config.component) {
        const Component = config.component;
        return <Component value={value} onChange={onChange} onClear={onClear} />;
      }
      return null;
      
    default:
      return null;
  }
}

// Filter popup component
function FilterPopup({
  filters,
  values,
  onChange,
  onClear,
  onClose
}: {
  filters: SearchFilterConfig[];
  values: SearchFilters;
  onChange: (key: string, value: string | number | boolean | SearchPriceRange | null | undefined) => void;
  onClear: (key: string) => void;
  onClose: () => void;
}) {
  const t = useTranslations('search');

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold">{t('advancedFilters')}</h3>
        <Button variant="ghost" size="sm" onClick={onClose}>
          <CloseIcon size={14} />
        </Button>
      </div>

      {filters.map((config) => (
        <div key={config.key} className="space-y-2">
          <label className="text-sm font-medium">{config.label}</label>
          
          {config.type === 'price-range' ? (
            <PriceRangeFilter
              value={values[config.key] as SearchPriceRange}
              onChange={(value) => onChange(config.key, value)}
              onClear={() => onClear(config.key)}
            />
          ) : (
            <FilterComponent
              config={config}
              value={values[config.key]}
              onChange={(value) => onChange(config.key, value)}
              onClear={() => onClear(config.key)}
            />
          )}
        </div>
      ))}
      
      <div className="flex gap-2 pt-4 border-t">
        <Button variant="outline" className="flex-1" onClick={onClose}>
          {t('apply')}
        </Button>
      </div>
    </div>
  );
}

// Price range filter component
function PriceRangeFilter({
  value,
  onChange,
  onClear
}: {
  value?: SearchPriceRange;
  onChange: (value: SearchPriceRange) => void;
  onClear: () => void;
}) {
  const t = useTranslations('search');
  const priceRange = value || { min: null, max: null };

  return (
    <div className="flex items-center gap-2">
      <Input
        type="number"
        value={priceRange.min || ''}
        onChange={(e) => onChange({ ...priceRange, min: Number(e.target.value) || null })}
        placeholder={t('priceFrom')}
        className="w-20"
      />
      <span className="text-muted-foreground">-</span>
      <Input
        type="number"
        value={priceRange.max || ''}
        onChange={(e) => onChange({ ...priceRange, max: Number(e.target.value) || null })}
        placeholder={t('priceTo')}
        className="w-20"
      />
      {(priceRange.min || priceRange.max) && (
        <Button variant="ghost" size="sm" onClick={onClear}>
          <CloseIcon size={12} />
        </Button>
      )}
    </div>
  );
}

// Filter chip component
function FilterChip({ 
  label, 
  onRemove 
}: {
  label: string;
  onRemove: () => void;
}) {
  return (
    <div className="inline-flex items-center gap-1 px-2 py-1 bg-muted rounded-[0.75rem] text-xs">
      <span>{label}</span>
      <button
        type="button"
        onClick={onRemove}
        className="text-muted-foreground hover:text-foreground cursor-pointer transition-colors"
        aria-label="Remove filter"
      >
        <CloseIcon size={10} />
      </button>
    </div>
  );
}

export default Search;