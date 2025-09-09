import { configureStore } from '@reduxjs/toolkit'
import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux'
import { persistStore, persistReducer } from 'redux-persist'
import storage from 'redux-persist/lib/storage'
import { combineReducers } from '@reduxjs/toolkit'
import { counterSlice } from '@/features/demo/stores/counterSlice'
import { userSettingsSlice } from '@/features/user/stores/userSettingsSlice'
import { toastSlice } from '@/shared/stores/toastSlice'
import { cartSlice } from '@/features/cart/stores/cartSlice'
import { favoritesSlice } from '@/features/favorites/stores/favoritesSlice'

// Persist configuration for counter
const counterPersistConfig = {
    key: 'counter',
    storage,
}

// Persist configuration for user settings
const userSettingsPersistConfig = {
    key: 'userSettings',
    storage,
}

// Persist configuration for cart
const cartPersistConfig = {
    key: 'cart',
    storage,
}

// Persist configuration for favorites
const favoritesPersistConfig = {
    key: 'favorites',
    storage,
}

// Create persisted reducers
const persistedCounterReducer = persistReducer(counterPersistConfig, counterSlice.reducer)
const persistedUserSettingsReducer = persistReducer(userSettingsPersistConfig, userSettingsSlice.reducer)
const persistedCartReducer = persistReducer(cartPersistConfig, cartSlice.reducer)
const persistedFavoritesReducer = persistReducer(favoritesPersistConfig, favoritesSlice.reducer)

// Root reducer
const rootReducer = combineReducers({
    counter: persistedCounterReducer,
    userSettings: persistedUserSettingsReducer,
    cart: persistedCartReducer,
    favorites: persistedFavoritesReducer,
    toast: toastSlice.reducer, // Toast doesn't need persistence
})

export const store = configureStore({
    reducer: rootReducer,
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
            serializableCheck: {
                ignoredActions: [
                    'persist/PERSIST',
                    'persist/REHYDRATE',
                    'persist/PAUSE',
                    'persist/PURGE',
                    'persist/REGISTER',
                ],
            },
        }),
})

export const persistor = persistStore(store)

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch

// Typed hooks
export const useAppDispatch = () => useDispatch<AppDispatch>()
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector
