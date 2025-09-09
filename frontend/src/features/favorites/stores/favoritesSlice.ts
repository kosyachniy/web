import { createSlice, PayloadAction } from '@reduxjs/toolkit'

export interface FavoritesState {
    items: number[]
    isInitialized: boolean
}

const initialState: FavoritesState = {
    items: [],
    isInitialized: false,
}

export const favoritesSlice = createSlice({
    name: 'favorites',
    initialState,
    reducers: {
        addToFavorites: (state, action: PayloadAction<number>) => {
            // Ensure items is always an array
            if (!Array.isArray(state.items)) {
                state.items = []
            }
            const productId = action.payload
            if (!state.items.includes(productId)) {
                state.items.push(productId)
            }
        },
        removeFromFavorites: (state, action: PayloadAction<number>) => {
            // Ensure items is always an array
            if (!Array.isArray(state.items)) {
                state.items = []
                return
            }
            const productId = action.payload
            state.items = state.items.filter(id => id !== productId)
        },
        toggleFavorite: (state, action: PayloadAction<number>) => {
            // Ensure items is always an array
            if (!Array.isArray(state.items)) {
                state.items = []
            }
            const productId = action.payload
            const index = state.items.indexOf(productId)
            
            if (index > -1) {
                state.items.splice(index, 1)
            } else {
                state.items.push(productId)
            }
        },
        clearFavorites: (state) => {
            state.items = []
        },
        loadFavoritesFromStorage: (state) => {
            // Load favorite items from localStorage on app initialization
            if (typeof window !== 'undefined') {
                const savedFavorites = localStorage.getItem('favoriteItems')
                if (savedFavorites) {
                    try {
                        const favoritesArray = JSON.parse(savedFavorites)
                        // Ensure loaded data is a valid array
                        state.items = Array.isArray(favoritesArray) ? favoritesArray : []
                    } catch (error) {
                        console.warn('Failed to parse favorites from localStorage:', error)
                        state.items = []
                    }
                } else {
                    state.items = []
                }
            } else {
                state.items = []
            }
            state.isInitialized = true
        },
        saveFavoritesToStorage: (state) => {
            // Save favorite items to localStorage
            if (typeof window !== 'undefined') {
                localStorage.setItem('favoriteItems', JSON.stringify(state.items))
            }
        },
    },
})

export const { 
    addToFavorites, 
    removeFromFavorites, 
    toggleFavorite, 
    clearFavorites, 
    loadFavoritesFromStorage, 
    saveFavoritesToStorage 
} = favoritesSlice.actions

// Selectors
export const selectFavoriteItems = (state: { favorites: FavoritesState }) => {
    const items = state.favorites?.items;
    return Array.isArray(items) ? items : [];
}

export const selectFavoriteItemsAsSet = (state: { favorites: FavoritesState }) => {
    const items = state.favorites?.items;
    return new Set(Array.isArray(items) ? items : []);
}

export const selectFavoritesCount = (state: { favorites: FavoritesState }) => {
    const items = state.favorites?.items;
    return Array.isArray(items) ? items.length : 0;
}

export const selectIsInFavorites = (productId: number) => (state: { favorites: FavoritesState }) => {
    const items = state.favorites?.items;
    return Array.isArray(items) ? items.includes(productId) : false;
}

export default favoritesSlice.reducer