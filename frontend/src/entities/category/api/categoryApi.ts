import { api } from '@/shared/services/api/client';
import { shouldUseMockFallback, logApiWarning, addMockDelay } from '@/shared/config/api';
import type { 
  Category, 
  CategoryTree, 
  CategoryWithSubcategories,
  CreateCategoryRequest, 
  UpdateCategoryRequest,
  GetCategoriesRequest 
} from '../model/category';

// Mock categories for development/fallback
const mockCategories: Category[] = [
  {
    id: 1,
    url: 'technology',
    title: 'Technology',
    description: 'Latest tech news and trends',
    status: 1,
    locale: 'en'
  },
  {
    id: 2,
    url: 'business',
    title: 'Business',
    description: 'Business insights and analysis',
    status: 1,
    locale: 'en'
  },
  {
    id: 3,
    url: 'lifestyle',
    title: 'Lifestyle',
    description: 'Lifestyle and culture content',
    status: 1,
    locale: 'en'
  }
];

interface CategoriesResponse {
  categories: Category[];
}

export async function getCategories(params: GetCategoriesRequest = {}): Promise<Category[]> {
  if (shouldUseMockFallback()) {
    try {
      // Use new REST endpoint with query parameters
      const queryParams = new URLSearchParams();
      if (params.locale) queryParams.append('locale', params.locale);
      if (params.parent !== undefined) queryParams.append('parent', params.parent.toString());
      if (params.status !== undefined) queryParams.append('status', params.status.toString());
      queryParams.append('include_tree', 'true'); // Get nested structure
      
      const response = await api.get<CategoriesResponse>(`/categories/?${queryParams.toString()}`);
      return response.categories || [];
    } catch (error) {
      logApiWarning('Categories API not available, using mock data', error);
      await addMockDelay();
      
      // Filter mock data based on parameters
      let filtered = [...mockCategories];
      
      if (params.locale) {
        filtered = filtered.filter(cat => cat.locale === params.locale);
      }
      
      if (params.parent !== undefined) {
        filtered = filtered.filter(cat => cat.parent === params.parent);
      }
      
      if (params.status !== undefined) {
        filtered = filtered.filter(cat => cat.status === params.status);
      }
      
      return filtered;
    }
  } else {
    // Production mode - use new REST endpoint
    const queryParams = new URLSearchParams();
    if (params.locale) queryParams.append('locale', params.locale);
    if (params.parent !== undefined) queryParams.append('parent', params.parent.toString());
    if (params.status !== undefined) queryParams.append('status', params.status.toString());
    queryParams.append('include_tree', 'true'); // Get nested structure
    
    const response = await api.get<CategoriesResponse>(`/categories/?${queryParams.toString()}`);
    return response.categories || [];
  }
}

export async function getCategoryTree(): Promise<CategoryTree[]> {
  if (shouldUseMockFallback()) {
    try {
      const response = await api.get<CategoriesResponse>('/categories/tree/');
      return response.categories as CategoryTree[] || [];
    } catch (error) {
      logApiWarning('Category tree API not available, using fallback', error);
      return [];
    }
  } else {
    const response = await api.get<CategoriesResponse>('/categories/tree/');
    return response.categories as CategoryTree[] || [];
  }
}

export async function getCategory(id: number): Promise<Category> {
  if (shouldUseMockFallback()) {
    try {
      const response = await api.get<Category>(`/categories/${id}/`);
      return response;
    } catch (error) {
      logApiWarning(`Category ${id} API not available, checking mock data`, error);
      const mockCategory = mockCategories.find(cat => cat.id === id);
      if (!mockCategory) {
        throw new Error('Category not found');
      }
      return mockCategory;
    }
  } else {
    return await api.get<Category>(`/categories/${id}/`);
  }
}

// Helper function to build the complete parent hierarchy for a category
function buildParentHierarchy(categories: Category[], targetCategory: Category): Array<{ id: number; url: string; title: string; }> {
  const parents: Array<{ id: number; url: string; title: string; }> = [];
  
  // Helper to find category by ID in nested structure
  const findCategoryById = (cats: Category[], id: number): Category | null => {
    for (const cat of cats) {
      if (cat.id === id) {
        return cat;
      }
      if (cat.categories && cat.categories.length > 0) {
        const found = findCategoryById(cat.categories, id);
        if (found) return found;
      }
    }
    return null;
  };
  
  // Build the path by traversing up through parent IDs
  let currentParentId = targetCategory.parent;
  
  while (currentParentId && currentParentId !== 0) {
    const parent = findCategoryById(categories, currentParentId);
    if (parent) {
      // Add to the beginning of the array to maintain correct order (root -> leaf)
      parents.unshift({
        id: parent.id,
        url: parent.url || '',
        title: parent.title
      });
      currentParentId = parent.parent;
    } else {
      break;
    }
  }
  
  return parents;
}

// Helper function to recursively search through nested categories by URL
// Internal recursive function that preserves the original full categories array
function findCategoryRecursive(categories: Category[], fullCategories: Category[], url: string): Category | null {
  for (const category of categories) {
    if (category.url === url) {
      // Add parent hierarchy to the found category using the ORIGINAL full categories array
      const categoryWithParents = {
        ...category,
        parents: buildParentHierarchy(fullCategories, category)
      };
      return categoryWithParents;
    }
    if (category.categories && category.categories.length > 0) {
      const found = findCategoryRecursive(category.categories, fullCategories, url);
      if (found) {
        return found;
      }
    }
  }
  return null;
}

// Public wrapper function
function findCategoryByUrlRecursive(categories: Category[], url: string): Category | null {
  return findCategoryRecursive(categories, categories, url);
}

// Helper function to recursively search through nested categories by ID
function findCategoryByIdRecursive(categories: Category[], id: number): Category | null {
  for (const category of categories) {
    if (category.id === id) {
      return category;
    }
    if (category.categories && category.categories.length > 0) {
      const found = findCategoryByIdRecursive(category.categories, id);
      if (found) {
        return found;
      }
    }
  }
  return null;
}

export async function getCategoryByUrl(url: string, locale?: string): Promise<Category | null> {
  try {
    // First try with the specified locale
    if (locale) {
      const categoriesWithLocale = await getCategories({ parent: 0, locale, status: 1, include_tree: true });
      const result = findCategoryByUrlRecursive(categoriesWithLocale, url);
      if (result) {
        return result;
      }
    }
    
    // Fallback: search without locale filter to find categories with different locales
    const allCategories = await getCategories({ parent: 0, status: 1, include_tree: true });
    return findCategoryByUrlRecursive(allCategories, url);
  } catch (error) {
    logApiWarning('Category lookup failed', error);
    return null;
  }
}

export async function getSubcategories(parentId?: number, locale?: string): Promise<Category[]> {
  if (parentId === undefined) {
    // Get top-level categories (parent: 0 in backend) with full tree structure
    // Try with locale first, then fallback to all categories
    if (locale) {
      const categoriesWithLocale = await getCategories({ parent: 0, locale, status: 1, include_tree: true });
      if (categoriesWithLocale.length > 0) {
        return categoriesWithLocale;
      }
    }
    // Fallback to all categories without locale filter
    return await getCategories({ parent: 0, status: 1, include_tree: true });
  } else {
    // Get direct subcategories using parent filter
    // Try with locale first, then fallback to all subcategories of this parent
    if (locale) {
      const subcategoriesWithLocale = await getCategories({ parent: parentId, locale, status: 1, include_tree: true });
      if (subcategoriesWithLocale.length > 0) {
        return subcategoriesWithLocale;
      }
    }
    // Fallback to all subcategories without locale filter
    return await getCategories({ parent: parentId, status: 1, include_tree: true });
  }
}

export async function getCategoryWithSubcategories(
  id: number, 
  locale?: string
): Promise<CategoryWithSubcategories> {
  const category = await getCategory(id);
  const subcategories = await getSubcategories(id, locale);
  return { ...category, subcategories };
}

export async function createCategory(data: CreateCategoryRequest): Promise<Category> {
  if (shouldUseMockFallback()) {
    try {
      const response = await api.post<Category>('/categories/', data);
      return response;
    } catch (error) {
      logApiWarning('Create category API not available, using mock response', error);
      await addMockDelay();
      
      // Return mock created category
      const newCategory: Category = {
        id: Math.max(...mockCategories.map(c => c.id)) + 1,
        url: data.title?.toLowerCase().replace(/\s+/g, '-') || 'new-category',
        title: data.title || 'New Category',
        description: data.description,
        parent: data.parent || 0,
        status: 1,
        locale: 'en',
        created: Date.now(),
        updated: Date.now()
      };
      
      mockCategories.push(newCategory);
      return newCategory;
    }
  } else {
    return api.post<Category>('/categories/', data);
  }
}

export async function updateCategory(id: number, data: UpdateCategoryRequest): Promise<Category> {
  if (shouldUseMockFallback()) {
    try {
      const response = await api.put<Category>(`/categories/${id}/`, data);
      return response;
    } catch (error) {
      logApiWarning(`Update category ${id} API not available, using mock response`, error);
      await addMockDelay();
      
      // Find and update mock category
      const categoryIndex = mockCategories.findIndex(cat => cat.id === id);
      if (categoryIndex === -1) {
        throw new Error('Category not found');
      }
      
      const updatedCategory = {
        ...mockCategories[categoryIndex],
        ...data,
        updated: Date.now()
      };
      
      mockCategories[categoryIndex] = updatedCategory;
      return updatedCategory;
    }
  } else {
    return api.put<Category>(`/categories/${id}/`, data);
  }
}

export async function deleteCategory(id: number): Promise<void> {
  if (shouldUseMockFallback()) {
    try {
      await api.delete(`/categories/${id}/`);
    } catch (error) {
      logApiWarning(`Delete category ${id} API not available, using mock response`, error);
      await addMockDelay();
      
      // Remove from mock data
      const categoryIndex = mockCategories.findIndex(cat => cat.id === id);
      if (categoryIndex === -1) {
        throw new Error('Category not found');
      }
      
      mockCategories.splice(categoryIndex, 1);
    }
  } else {
    await api.delete(`/categories/${id}/`);
  }
}