// Category entity types
export interface Category {
  id: number;
  url: string;
  title: string;
  description?: string;
  image?: string;
  data?: string;
  locale?: string;
  created?: number;
  updated?: number;
  status?: number;
  parent?: number;
  user?: number;
  post_count?: number; // Number of posts in this category
  parents?: Array<{
    id: number;
    url: string;
    title: string;
  }>;
  categories?: Category[]; // Nested subcategories from backend
}

export interface CategoryTree extends Category {
  children?: CategoryTree[];
  depth?: number;
}

export interface CreateCategoryRequest {
  title: string;
  url?: string;
  description?: string;
  data?: string; // JSON metadata
  image?: string;
  parent?: number;
  locale?: string;
  status?: number;
}

export interface UpdateCategoryRequest {
  title?: string;
  url?: string;
  description?: string;
  data?: string; // JSON metadata
  image?: string;
  parent?: number;
  locale?: string;
  status?: number;
}

export interface GetCategoriesRequest {
  locale?: string;
  parent?: number;
  status?: number;
}

export interface CategoryWithSubcategories extends Category {
  subcategories?: Category[];
}