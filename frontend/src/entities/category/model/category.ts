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
  description?: string;
  parent?: number;
}

export interface UpdateCategoryRequest {
  title?: string;
  description?: string;
  parent?: number;
}

export interface GetCategoriesRequest {
  locale?: string;
  parent?: number;
  status?: number;
}

export interface CategoryWithSubcategories extends Category {
  subcategories?: Category[];
}