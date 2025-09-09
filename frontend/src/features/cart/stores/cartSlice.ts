import { createSlice, PayloadAction } from '@reduxjs/toolkit'

export interface CartState {
    items: number[]
    isInitialized: boolean
}

const initialState: CartState = {
    items: [],
    isInitialized: false,
}

export const cartSlice = createSlice({
    name: 'cart',
    initialState,
    reducers: {
        addToCart: (state, action: PayloadAction<number>) => {
            // Ensure items is always an array
            if (!Array.isArray(state.items)) {
                state.items = []
            }
            const productId = action.payload
            if (!state.items.includes(productId)) {
                state.items.push(productId)
            }
        },
        removeFromCart: (state, action: PayloadAction<number>) => {
            // Ensure items is always an array
            if (!Array.isArray(state.items)) {
                state.items = []
                return
            }
            const productId = action.payload
            state.items = state.items.filter(id => id !== productId)
        },
        toggleCartItem: (state, action: PayloadAction<number>) => {
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
        clearCart: (state) => {
            state.items = []
        },
        loadCartFromStorage: (state) => {
            // Load cart items from localStorage on app initialization
            if (typeof window !== 'undefined') {
                const savedCart = localStorage.getItem('cartItems')
                if (savedCart) {
                    try {
                        const cartArray = JSON.parse(savedCart)
                        // Ensure loaded data is a valid array
                        state.items = Array.isArray(cartArray) ? cartArray : []
                    } catch (error) {
                        console.warn('Failed to parse cart from localStorage:', error)
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
        saveCartToStorage: (state) => {
            // Save cart items to localStorage
            if (typeof window !== 'undefined') {
                localStorage.setItem('cartItems', JSON.stringify(state.items))
            }
        },
    },
})

export const { 
    addToCart, 
    removeFromCart, 
    toggleCartItem, 
    clearCart, 
    loadCartFromStorage, 
    saveCartToStorage 
} = cartSlice.actions

// Selectors
export const selectCartItems = (state: { cart: CartState }) => {
    const items = state.cart?.items;
    return Array.isArray(items) ? items : [];
}

export const selectCartItemsAsSet = (state: { cart: CartState }) => {
    const items = state.cart?.items;
    return new Set(Array.isArray(items) ? items : []);
}

export const selectCartCount = (state: { cart: CartState }) => {
    const items = state.cart?.items;
    return Array.isArray(items) ? items.length : 0;
}

export const selectIsInCart = (productId: number) => (state: { cart: CartState }) => {
    const items = state.cart?.items;
    return Array.isArray(items) ? items.includes(productId) : false;
}

export default cartSlice.reducer