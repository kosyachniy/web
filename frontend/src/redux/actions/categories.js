export const categoriesGet = (categories) => ({
  type: 'CATEGORIES_GET',
  categories,
});

export const categoriesAdd = (category) => ({
  type: 'CATEGORIES_ADD',
  category,
});

export const categoriesClear = () => ({
  type: 'CATEGORIES_CLEAR',
});
