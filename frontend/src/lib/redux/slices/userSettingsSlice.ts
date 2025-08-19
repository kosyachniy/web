import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import type { Locale } from '@/i18n/routing'

export interface UserSettings {
    language: Locale
    theme: 'light' | 'dark' | 'system'
    isInitialized: boolean
    // Add more user preferences here in the future
}

const initialState: UserSettings = {
    language: 'en', // Default language
    theme: 'system',
    isInitialized: false,
}

export const userSettingsSlice = createSlice({
    name: 'userSettings',
    initialState,
    reducers: {
        setLanguage: (state, action: PayloadAction<Locale>) => {
            state.language = action.payload
            // Store in localStorage for persistence
            if (typeof window !== 'undefined') {
                localStorage.setItem('userLanguage', action.payload)
            }
        },
        setTheme: (state, action: PayloadAction<'light' | 'dark' | 'system'>) => {
            state.theme = action.payload
            // Store in localStorage for persistence
            if (typeof window !== 'undefined') {
                localStorage.setItem('userTheme', action.payload)
            }
        },
        loadSettings: (state) => {
            // Load settings from localStorage on app initialization
            if (typeof window !== 'undefined') {
                const savedLanguage = localStorage.getItem('userLanguage') as Locale
                const savedTheme = localStorage.getItem('userTheme') as 'light' | 'dark' | 'system'

                if (savedLanguage && ['en', 'ru', 'zh', 'es', 'ar'].includes(savedLanguage)) {
                    state.language = savedLanguage
                }

                if (savedTheme && ['light', 'dark', 'system'].includes(savedTheme)) {
                    state.theme = savedTheme
                }
            }
            // Mark as initialized regardless of whether we found saved settings
            state.isInitialized = true
        },
        resetSettings: (state) => {
            state.language = 'en'
            state.theme = 'system'
            state.isInitialized = true
            // Clear localStorage
            if (typeof window !== 'undefined') {
                localStorage.removeItem('userLanguage')
                localStorage.removeItem('userTheme')
            }
        },
    },
})

export const { setLanguage, setTheme, loadSettings, resetSettings } = userSettingsSlice.actions

export default userSettingsSlice.reducer
