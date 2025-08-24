import { configureStore } from '@reduxjs/toolkit'
import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux'
import { counterSlice } from '@/features/demo/stores/counterSlice'
import { userSettingsSlice } from '@/features/user/stores/userSettingsSlice'
import { toastSlice } from '@/shared/stores/toastSlice'

export const store = configureStore({
    reducer: {
        counter: counterSlice.reducer,
        userSettings: userSettingsSlice.reducer,
        toast: toastSlice.reducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
            serializableCheck: {
                ignoredActions: ['persist/PERSIST'],
            },
        }),
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch

// Typed hooks
export const useAppDispatch = () => useDispatch<AppDispatch>()
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector
