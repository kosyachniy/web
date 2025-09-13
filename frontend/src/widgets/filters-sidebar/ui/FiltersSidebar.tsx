'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import { SidebarCard } from '@/shared/ui/sidebar-card';
import { IconButton } from '@/shared/ui/icon-button';
import { ButtonGroup } from '@/shared/ui/button-group';
import { Input } from '@/shared/ui/input';
import { RangeSlider } from '@/shared/ui/range-slider';
import Popup from '@/widgets/feedback-system/ui/Popup';
import { DateCalendar, DateRange } from '@/shared/ui/date-calendar';
import { ChevronRightIcon, ChevronDownIcon } from '@/shared/ui/icons';
import {
  FilterIcon,
  CalendarIcon,
  XIcon,
  ClothingIcon,
  ElectronicsIcon,
  HomeGardenIcon,
  AutoMotoIcon,
  FoodBeverageIcon,
  BeautyHealthIcon,
  BagsAccessoriesIcon,
  HobbiesCreativityIcon,
  StarIcon
} from '@/shared/ui/icons';

interface FiltersSidebarProps {
  className?: string;
}

interface Category {
  id: number;
  title: string;
  icon: React.ReactNode;
  parent?: number;
  categories?: Category[];
}

// Helper function to format date as DD.MM.YYYY
const formatDateForDisplay = (date: Date): string => {
  const day = String(date.getDate()).padStart(2, '0')
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const year = date.getFullYear()
  return `${day}.${month}.${year}`
}

export default function FiltersSidebar({ className }: FiltersSidebarProps) {
  const t = useTranslations('filters');

  // Date range states
  const [dateRange, setDateRange] = useState<DateRange | undefined>();
  const [tempDateRange, setTempDateRange] = useState<DateRange | undefined>();
  const [isDatePickerOpen, setIsDatePickerOpen] = useState(false);

  // Price range states
  const [priceRange, setPriceRange] = useState<number[]>([0, 500]);
  const [minPriceInput, setMinPriceInput] = useState<string>('0');
  const [maxPriceInput, setMaxPriceInput] = useState<string>('500');

  // Rating states
  const [selectedRating, setSelectedRating] = useState<number>(0);

  // Category states
  const [selectedCategories, setSelectedCategories] = useState<number[]>([]);
  const [openCategories, setOpenCategories] = useState<number[]>([]);

  // Time filter shortcuts organized in 4 groups
  const timeFilterGroups = [
    {
      title: t('lastPeriods'),
      filters: [
        { key: 'lastDay', label: t('lastDay') },
        { key: 'lastWeek', label: t('lastWeek') },
        { key: 'lastMonth', label: t('lastMonth') },
        { key: 'lastYear', label: t('lastYear') }
      ]
    },
    {
      title: t('currentPeriods'),
      filters: [
        { key: 'today', label: t('today') },
        { key: 'currentWeek', label: t('currentWeekFromMonday') },
        { key: 'thisMonth', label: t('thisMonth') },
        { key: 'thisYear', label: t('thisYear') }
      ]
    },
    {
      title: t('previousPeriods'),
      filters: [
        { key: 'yesterday', label: t('yesterday') },
        { key: 'previousWeek', label: t('previousWeek') },
        { key: 'previousMonth', label: t('previousMonth') },
        { key: 'previousYear', label: t('previousYear') }
      ]
    }
  ];

  // Categories with icons and nested structure based on user's catalog
  const categories: Category[] = [
    {
      id: 1,
      title: t('clothingFootwear'),
      icon: <ClothingIcon size={16} />,
      categories: [
        { id: 11, title: t('mensClothing'), parent: 1, icon: <ClothingIcon size={14} /> },
        { id: 12, title: t('womensClothing'), parent: 1, icon: <ClothingIcon size={14} /> },
        { id: 13, title: t('childrensClothing'), parent: 1, icon: <ClothingIcon size={14} /> },
        { id: 14, title: t('shoes'), parent: 1, icon: <ClothingIcon size={14} /> },
        { id: 15, title: t('sportswear'), parent: 1, icon: <ClothingIcon size={14} /> }
      ]
    },
    {
      id: 2,
      title: t('bagsAccessories'),
      icon: <BagsAccessoriesIcon size={16} />,
      categories: [
        { id: 21, title: t('handbags'), parent: 2, icon: <BagsAccessoriesIcon size={14} /> },
        { id: 22, title: t('backpacks'), parent: 2, icon: <BagsAccessoriesIcon size={14} /> },
        { id: 23, title: t('jewelry'), parent: 2, icon: <BagsAccessoriesIcon size={14} /> },
        { id: 24, title: t('watches'), parent: 2, icon: <BagsAccessoriesIcon size={14} /> },
        { id: 25, title: t('sunglasses'), parent: 2, icon: <BagsAccessoriesIcon size={14} /> }
      ]
    },
    {
      id: 3,
      title: t('electronics'),
      icon: <ElectronicsIcon size={16} />,
      categories: [
        { id: 31, title: t('smartphones'), parent: 3, icon: <ElectronicsIcon size={14} /> },
        { id: 32, title: t('laptops'), parent: 3, icon: <ElectronicsIcon size={14} /> },
        { id: 33, title: t('tablets'), parent: 3, icon: <ElectronicsIcon size={14} /> },
        { id: 34, title: t('headphones'), parent: 3, icon: <ElectronicsIcon size={14} /> },
        { id: 35, title: t('cameras'), parent: 3, icon: <ElectronicsIcon size={14} /> }
      ]
    },
    {
      id: 4,
      title: t('healthBeauty'),
      icon: <BeautyHealthIcon size={16} />,
      categories: [
        { id: 41, title: t('skincare'), parent: 4, icon: <BeautyHealthIcon size={14} /> },
        { id: 42, title: t('makeup'), parent: 4, icon: <BeautyHealthIcon size={14} /> },
        { id: 43, title: t('perfumes'), parent: 4, icon: <BeautyHealthIcon size={14} /> },
        { id: 44, title: t('haircare'), parent: 4, icon: <BeautyHealthIcon size={14} /> },
        { id: 45, title: t('supplements'), parent: 4, icon: <BeautyHealthIcon size={14} /> }
      ]
    },
    {
      id: 5,
      title: t('homeGarden'),
      icon: <HomeGardenIcon size={16} />,
      categories: [
        { id: 51, title: t('furniture'), parent: 5, icon: <HomeGardenIcon size={14} /> },
        { id: 52, title: t('decor'), parent: 5, icon: <HomeGardenIcon size={14} /> },
        { id: 53, title: t('kitchenware'), parent: 5, icon: <HomeGardenIcon size={14} /> },
        { id: 54, title: t('gardenTools'), parent: 5, icon: <HomeGardenIcon size={14} /> },
        { id: 55, title: t('lighting'), parent: 5, icon: <HomeGardenIcon size={14} /> }
      ]
    },
    {
      id: 6,
      title: t('autoMoto'),
      icon: <AutoMotoIcon size={16} />,
      categories: [
        { id: 61, title: t('carAccessories'), parent: 6, icon: <AutoMotoIcon size={14} /> },
        { id: 62, title: t('carParts'), parent: 6, icon: <AutoMotoIcon size={14} /> },
        { id: 63, title: t('motorcycle'), parent: 6, icon: <AutoMotoIcon size={14} /> },
        { id: 64, title: t('tools'), parent: 6, icon: <AutoMotoIcon size={14} /> },
        { id: 65, title: t('oils'), parent: 6, icon: <AutoMotoIcon size={14} /> }
      ]
    },
    {
      id: 7,
      title: t('hobbiesCreativity'),
      icon: <HobbiesCreativityIcon size={16} />,
      categories: [
        { id: 71, title: t('artSupplies'), parent: 7, icon: <HobbiesCreativityIcon size={14} /> },
        { id: 72, title: t('crafts'), parent: 7, icon: <HobbiesCreativityIcon size={14} /> },
        { id: 73, title: t('musicalInstruments'), parent: 7, icon: <HobbiesCreativityIcon size={14} /> },
        { id: 74, title: t('collectibles'), parent: 7, icon: <HobbiesCreativityIcon size={14} /> },
        { id: 75, title: t('books'), parent: 7, icon: <HobbiesCreativityIcon size={14} /> }
      ]
    },
    {
      id: 8,
      title: t('foodBeverage'),
      icon: <FoodBeverageIcon size={16} />,
      categories: [
        { id: 81, title: t('beverages'), parent: 8, icon: <FoodBeverageIcon size={14} /> },
        { id: 82, title: t('snacks'), parent: 8, icon: <FoodBeverageIcon size={14} /> },
        { id: 83, title: t('organic'), parent: 8, icon: <FoodBeverageIcon size={14} /> },
        { id: 84, title: t('spices'), parent: 8, icon: <FoodBeverageIcon size={14} /> },
        { id: 85, title: t('gourmet'), parent: 8, icon: <FoodBeverageIcon size={14} /> }
      ]
    }
  ];

  // Control points for price slider
  const priceControlPoints = [0, 50, 100, 250, 500];

  // Rating options as fast buttons - sorted in descending order
  const ratingOptions = [4.9, 4.7, 4.5, 4.0, 3.5, 3.0];

  // Auto-select subcategories when parent is selected
  const handleCategorySelect = (categoryId: number) => {
    const category = findCategoryById(categoryId, categories);
    if (!category) return;

    const newSelection = [...selectedCategories];

    if (selectedCategories.includes(categoryId)) {
      // Unselect category and all subcategories
      const toRemove = [categoryId];
      if (category.categories) {
        toRemove.push(...category.categories.map(sub => sub.id));
      }
      setSelectedCategories(newSelection.filter(id => !toRemove.includes(id)));
    } else {
      // Select category and all subcategories
      const toAdd = [categoryId];
      if (category.categories) {
        toAdd.push(...category.categories.map(sub => sub.id));
      }
      setSelectedCategories([...newSelection, ...toAdd]);
    }
  };

  const findCategoryById = (id: number, cats: Category[]): Category | undefined => {
    for (const cat of cats) {
      if (cat.id === id) return cat;
      if (cat.categories) {
        const found = findCategoryById(id, cat.categories);
        if (found) return found;
      }
    }
    return undefined;
  };

  const toggleCategory = (categoryId: number) => {
    if (openCategories.includes(categoryId)) {
      setOpenCategories(openCategories.filter(id => id !== categoryId));
    } else {
      setOpenCategories([...openCategories, categoryId]);
    }
  };


  const handleTempTimeFilterClick = (key: string) => {
    const now = new Date();
    let from: Date | undefined;
    let to: Date | undefined = now;

    switch (key) {
      case 'today':
        from = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        break;
      case 'yesterday':
        const yesterday = new Date(now.getTime() - 24 * 60 * 60 * 1000);
        from = new Date(yesterday.getFullYear(), yesterday.getMonth(), yesterday.getDate());
        to = new Date(yesterday.getFullYear(), yesterday.getMonth(), yesterday.getDate(), 23, 59, 59);
        break;
      case 'currentWeek':
        // Get Monday of current week
        const dayOfWeek = now.getDay();
        const daysFromMonday = dayOfWeek === 0 ? 6 : dayOfWeek - 1;
        from = new Date(now.getTime() - daysFromMonday * 24 * 60 * 60 * 1000);
        from = new Date(from.getFullYear(), from.getMonth(), from.getDate());
        break;
      case 'lastWeek':
        // Exactly 7 days ago
        from = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
        break;
      case 'thisMonth':
        from = new Date(now.getFullYear(), now.getMonth(), 1);
        break;
      case 'lastMonth':
        // Last 30 days (rolling period)
        from = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
        break;
      case 'thisYear':
        from = new Date(now.getFullYear(), 0, 1);
        break;
      case 'lastYear':
        // Last 365 days (rolling period)
        from = new Date(now.getTime() - 365 * 24 * 60 * 60 * 1000);
        break;
      case 'lastDay':
        // Last 24 hours
        from = new Date(now.getTime() - 24 * 60 * 60 * 1000);
        break;
      case 'previousWeek':
        // Previous week from Monday to Sunday
        const prevWeekEnd = new Date(now.getTime() - (now.getDay() === 0 ? 0 : now.getDay()) * 24 * 60 * 60 * 1000);
        prevWeekEnd.setHours(0, 0, 0, 0);
        const prevWeekStart = new Date(prevWeekEnd.getTime() - 6 * 24 * 60 * 60 * 1000);
        from = prevWeekStart;
        to = new Date(prevWeekEnd.getTime() + 24 * 60 * 60 * 1000 - 1);
        break;
      case 'previousMonth':
        // Previous month from 1st to last day
        const prevMonth = new Date(now.getFullYear(), now.getMonth() - 1, 1);
        from = prevMonth;
        to = new Date(now.getFullYear(), now.getMonth(), 0, 23, 59, 59);
        break;
      case 'previousYear':
        // Previous year from Jan 1st to Dec 31st
        from = new Date(now.getFullYear() - 1, 0, 1);
        to = new Date(now.getFullYear() - 1, 11, 31, 23, 59, 59);
        break;
      case 'all':
        from = undefined;
        to = undefined;
        break;
      case 'reset':
        setTempDateRange(undefined);
        return;
    }

    setTempDateRange({ from, to });
  };

  const handlePriceInputChange = (type: 'min' | 'max', value: string) => {
    const numValue = parseInt(value) || 0;
    if (type === 'min') {
      setMinPriceInput(value);
      setPriceRange([numValue, priceRange[1]]);
    } else {
      setMaxPriceInput(value);
      setPriceRange([priceRange[0], numValue]);
    }
  };

  const handlePriceRangeChange = (values: number[]) => {
    setPriceRange(values);
    setMinPriceInput(values[0].toString());
    setMaxPriceInput(values[1].toString());
  };

  const renderCategoryTree = (cats: Category[], level = 0) => {
    return cats.map((category) => (
      <div key={category.id} className="space-y-0.5">
        <div className={`flex items-center space-x-1 ${level > 0 ? 'ml-6' : ''}`}>
          {category.categories && category.categories.length > 0 ? (
            <button
              onClick={() => toggleCategory(category.id)}
              className="w-6 h-6 flex items-center justify-center hover:bg-muted/50 rounded-sm transition-colors cursor-pointer"
            >
              {openCategories.includes(category.id) ? (
                <ChevronDownIcon size={12} />
              ) : (
                <ChevronRightIcon size={12} />
              )}
            </button>
          ) : (
            <div className="w-6 h-6" />
          )}

          <label className="flex items-center space-x-2.5 flex-1 cursor-pointer group">
            <input
              type="checkbox"
              checked={selectedCategories.includes(category.id)}
              onChange={() => handleCategorySelect(category.id)}
              className="rounded border-gray-300 text-primary focus:ring-primary w-4 h-4 cursor-pointer"
            />
            <div className="flex items-center space-x-1.5 group-hover:text-foreground transition-colors">
              <span className="text-muted-foreground">{category.icon}</span>
              <span className="text-sm font-medium">{category.title}</span>
            </div>
          </label>
        </div>

        {category.categories &&
          category.categories.length > 0 &&
          openCategories.includes(category.id) && (
            <div className="space-y-0.5">
              {renderCategoryTree(category.categories, level + 1)}
            </div>
          )}
      </div>
    ));
  };

  const clearAllFilters = () => {
    setDateRange(undefined);
    setPriceRange([0, 500]);
    setMinPriceInput('0');
    setMaxPriceInput('500');
    setSelectedRating(0);
    setSelectedCategories([]);
  };

  return (
    <SidebarCard
      title={t('filters')}
      icon={<FilterIcon size={20} />}
      className={className}
    >
      <div className="space-y-6">
        {/* Categories Block */}
        <div className="space-y-3">
          <h4 className="font-medium text-sm text-muted-foreground uppercase tracking-wide">
            {t('categories')}
          </h4>
          <div className="space-y-1 max-h-64 overflow-y-auto">
            {renderCategoryTree(categories)}
          </div>
        </div>

        {/* Date Range Block */}
        <div className="space-y-3">
          <h4 className="font-medium text-sm text-muted-foreground uppercase tracking-wide">
            {t('timeRange')}
          </h4>

          <IconButton
            variant="outline"
            size="sm"
            className="w-full justify-start"
            icon={<CalendarIcon size={16} />}
            onClick={() => {
              setTempDateRange(dateRange);
              setIsDatePickerOpen(true);
            }}
          >
            {dateRange?.from ? (
              dateRange.to ? (
                `${formatDateForDisplay(dateRange.from)} - ${formatDateForDisplay(dateRange.to)}`
              ) : (
                formatDateForDisplay(dateRange.from)
              )
            ) : (
              t('selectDate')
            )}
          </IconButton>

          {/* Date Picker Popup */}
          <Popup
            isOpen={isDatePickerOpen}
            onClose={() => setIsDatePickerOpen(false)}
            title={t('selectDate')}
            size="md"
          >
            <div className="space-y-4">
              <DateCalendar
                selected={tempDateRange}
                onSelect={setTempDateRange}
              />

              {/* Quick Date Buttons */}
              <div className="space-y-3">
                <h5 className="text-sm font-medium">{t('quickSelect')}</h5>
                <div className="space-y-3">
                  {timeFilterGroups.map((group, groupIndex) => (
                    <div key={groupIndex} className="space-y-2">
                      <h6 className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
                        {group.title}
                      </h6>
                      <div className="grid grid-cols-2 gap-2">
                        {group.filters.map((filter) => (
                          <button
                            key={filter.key}
                            onClick={() => handleTempTimeFilterClick(filter.key)}
                            className="text-xs p-2 bg-muted/50 hover:bg-muted rounded-[0.75rem] transition-colors cursor-pointer"
                          >
                            {filter.label}
                          </button>
                        ))}
                      </div>
                    </div>
                  ))}

                  {/* Action Buttons */}
                  <div className="pt-2 border-t">
                    <div className="grid grid-cols-3 gap-2">
                      <button
                        onClick={() => setIsDatePickerOpen(false)}
                        className="text-xs p-2 bg-muted/50 hover:bg-muted text-muted-foreground rounded-[0.75rem] transition-colors cursor-pointer font-medium"
                      >
                        {t('cancel')}
                      </button>
                      <button
                        onClick={() => {
                          setDateRange(tempDateRange);
                          setIsDatePickerOpen(false);
                        }}
                        className="text-xs p-2 bg-primary hover:bg-primary/90 text-primary-foreground rounded-[0.75rem] transition-colors cursor-pointer font-medium"
                      >
                        {t('apply')}
                      </button>
                      <button
                        onClick={() => handleTempTimeFilterClick('reset')}
                        className="text-xs p-2 bg-destructive/10 hover:bg-destructive/20 text-destructive rounded-[0.75rem] transition-colors cursor-pointer font-medium"
                      >
                        {t('reset')}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </Popup>
        </div>

        {/* Price Range Block */}
        <div className="space-y-3">
          <h4 className="font-medium text-sm text-muted-foreground uppercase tracking-wide">
            {t('priceRange')}
          </h4>

          {/* Price Inputs */}
          <div className="flex space-x-2">
            <Input
              type="number"
              placeholder={t('minPrice')}
              value={minPriceInput}
              onChange={(e) => handlePriceInputChange('min', e.target.value)}
              className="text-sm"
            />
            <Input
              type="number"
              placeholder={t('maxPrice')}
              value={maxPriceInput}
              onChange={(e) => handlePriceInputChange('max', e.target.value)}
              className="text-sm"
            />
          </div>

          {/* Price Range Slider */}
          <div className="px-2 mb-11">
            <RangeSlider
              value={priceRange}
              onValueChange={handlePriceRangeChange}
              min={0}
              max={500}
              step={5}
              controlPoints={priceControlPoints}
              formatValue={(v) => `$${v}`}
              className="w-full cursor-pointer"
            />
          </div>
        </div>

        {/* Rating Block */}
        <div className="space-y-3">
          <h4 className="font-medium text-sm text-muted-foreground uppercase tracking-wide">
            {t('rating')}
          </h4>

          <div className="grid grid-cols-3 gap-2">
            {ratingOptions.map((rating) => (
              <button
                key={rating}
                onClick={() => setSelectedRating(rating === selectedRating ? 0 : rating)}
                className={`flex items-center justify-center space-x-1 p-2 rounded-[0.75rem] text-xs transition-colors cursor-pointer ${selectedRating === rating
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-muted/50 hover:bg-muted text-muted-foreground'
                  }`}
              >
                {selectedRating === rating ? (
                  <StarIcon size={12} className="text-primary-foreground" />
                ) : (
                  <StarIcon size={12} className="text-yellow-500" />
                )}
                <span>⩾{rating.toFixed(1)}</span>
              </button>
            ))}
          </div>

          {selectedRating > 0 && (
            <div className="text-xs text-muted-foreground text-center">
              ⩾{selectedRating.toFixed(1)} {t('ratingAndUp')}
            </div>
          )}
        </div>

        {/* Clear Filters */}
        <div className="pt-4 border-t">
          <ButtonGroup className="w-full">
            <IconButton
              icon={<XIcon size={14} />}
              variant="outline"
              size="sm"
              className="flex-1"
              onClick={clearAllFilters}
              responsive
            >
              {t('clearFilters')}
            </IconButton>
          </ButtonGroup>
        </div>
      </div>
    </SidebarCard>
  );
}
