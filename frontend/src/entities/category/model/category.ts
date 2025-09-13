// Category entity types
export interface Category {
  id: number;
  url: string;
  title: string;
  description?: string;
  image?: string;
  icon?: string; // FontAwesome icon key
  color?: string; // Hex color code
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
  image?: string;
  parent?: number;
  locale?: string;
  status?: number;
  icon?: string; // FontAwesome icon key
  color?: string; // Hex color code
}

export interface UpdateCategoryRequest {
  title?: string;
  url?: string;
  description?: string;
  image?: string;
  parent?: number;
  locale?: string;
  status?: number;
  icon?: string; // FontAwesome icon key
  color?: string; // Hex color code
}

export interface GetCategoriesRequest {
  locale?: string;
  parent?: number;
  status?: number;
  include_tree?: boolean;
}

export interface CategoryWithSubcategories extends Category {
  subcategories?: Category[];
}