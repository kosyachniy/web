import { configureStore } from '@reduxjs/toolkit'
import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux'
import { persistStore, persistReducer } from 'redux-persist'
import storage from 'redux-persist/lib/storage'
import { combineReducers } from '@reduxjs/toolkit'
import { counterSlice } from '@/features/demo/stores/counterSlice'
import { userSettingsSlice } from '@/features/user/stores/userSettingsSlice'
import { toastSlice } from '@/shared/stores/toastSlice'

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

// Create persisted reducers
const persistedCounterReducer = persistReducer(counterPersistConfig, counterSlice.reducer)
const persistedUserSettingsReducer = persistReducer(userSettingsPersistConfig, userSettingsSlice.reducer)

// Root reducer
const rootReducer = combineReducers({
    counter: persistedCounterReducer,
    userSettings: persistedUserSettingsReducer,
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
