export { 
    favoritesSlice, 
    addToFavorites, 
    removeFromFavorites, 
    toggleFavorite, 
    clearFavorites, 
    loadFavoritesFromStorage, 
    saveFavoritesToStorage,
    selectFavoriteItems,
    selectFavoriteItemsAsSet,
    selectFavoritesCount,
    selectIsInFavorites
} from './stores/favoritesSlice'
export type { FavoritesState } from './stores/favoritesSlice'