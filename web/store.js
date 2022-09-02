import { useMemo } from 'react'
import { combineReducers, createStore, applyMiddleware } from 'redux'
import { composeWithDevTools } from '@redux-devtools/extension'
import { persistReducer } from 'redux-persist'
import storage from 'redux-persist/lib/storage'

import { generate } from './functions/generate'

let store


// actions.js

export const postsGet = posts => ({
    type: 'POSTS_GET',
    posts,
})

export const postsAdd = post => ({
    type: 'POSTS_ADD',
    post,
})

export const postsEdit = post => ({
    type: 'POSTS_EDIT',
    post,
})

export const postsDelete = id => ({
    type: 'POSTS_DELETE',
    id,
})

export const onlineAdd = online => ({
    type: 'ONLINE_ADD',
    count: online.count,
    users: online.users,
})

export const onlineDelete = online => ({
    type: 'ONLINE_DELETE',
    count: online.count,
    ids: online.users.map(user => user.id),
})

export const onlineReset = () => ({
    type: 'ONLINE_RESET',
})

export const changeTheme = theme => ({
    type: 'CHANGE_THEME',
    theme,
    color: theme === 'dark' ? 'light' : 'dark',
})

export const searching = search => ({
    type: 'SEARCH',
    search,
})

export const changeLang = locale => ({
    type: 'CHANGE_LANG',
    locale,  // i18n.changeLanguage(locale)
})

export const profileIn = ({ id, login, avatar, name, surname, phone, mail, social, status }) => ({
    type: 'PROFILE_IN',
    id, login, avatar, name, surname, phone, mail, social, status,
})

export const profileOut = () => ({
    type: 'PROFILE_OUT',
})

export const profileUpdate = profile => ({
    type: 'PROFILE_UPDATE',
    profile,
})

export const systemLoaded = () => ({
    type: 'SYSTEM_LOADED',
})

export const popupSet = popup => ({
    type: 'SYSTEM_POPUP',
    popup,
})

// reducers.js

export const system = (state = {
    token: generate(),
    locale: 'en',
    theme: null,
    color: null,
    search: null,
    loaded: false,
    popup: null,
}, action) => {
    switch (action.type) {
        case 'CHANGE_THEME':
            return {
                ...state,
                theme: action.theme,
                color: action.color,
            };

        case 'CHANGE_LANG':
            return {
                ...state,
                locale: action.locale,
            };

        case 'SYSTEM_LOADED':
            return {
                ...state,
                loaded: true,
            };

        case 'SYSTEM_POPUP':
            return {
                ...state,
                popup: action.popup,
            };

        case 'SEARCH':
            return {
                ...state,
                search: action.search,
            }

        default:
            return {
                token: state.token || generate(),
                locale: state.locale || process.env.NEXT_PUBLIC_LOCALE,
                theme: state.theme || 'light',
                color: state.color || 'dark',
                search: state.search || '',
                loaded: state.loaded,
                popup: state.popup,
            };
    }
}

export const posts = (state = [], action) => {
    switch (action.type) {
        case 'POSTS_GET':
            return action.posts;

        case 'POSTS_ADD':
            return [
                action.post,
                ...state
            ];

        case 'POSTS_EDIT':
            return state.map(post => {
                if (post.id === action.post.id) {
                    ['title', 'data'].map(el => {
                        if (el in action.post) {
                            post[el] = action.post[el]
                        }

                        return null;
                    })
                }

                return post;
            })

        case 'POSTS_DELETE':
            return state.filter(note => note.id !== action.id);

        default:
            return state;
    }
}

export const online = (state = {count: null, users: []}, action) => {
    switch (action.type) {
        case 'ONLINE_ADD':
            return {
                count: action.count,
                users: [
                    ...action.users,
                    ...state.users
                ]
            };

        case 'ONLINE_DELETE':
            return {
                count: action.count,
                users: state.users.filter(user => action.ids.indexOf(user.id) === -1),
            };

        case 'ONLINE_RESET':
            return {count: null, users: []};

        default:
            return state;
    }
}

export const profile = (state = {
    id: 0,
    login: null,
    name: null,
    surname: null,
    mail: null,
    avatar: null,
    avatar_optimize: null,
    admin: 2,
}, action) => {
    switch (action.type) {
        case 'PROFILE_IN':
            return {
                id: action.id,
                login: action.login,
                name: action.name,
                surname: action.surname,
                mail: action.mail,
                avatar: action.avatar || '/user.png',
                avatar_optimize: action.avatar || '/user.png',
                admin: action.admin,
            };

        case 'PROFILE_OUT':
            return {
                id: 0,
                login: null,
                name: null,
                surname: null,
                mail: null,
                avatar: null,
                avatar_optimize: null,
                admin: 2,
            };

        case 'PROFILE_UPDATE':
            if (action.profile.login) {
                state.login = action.profile.login
            }
            if (action.profile.name) {
                state.name = action.profile.name
            }
            if (action.profile.surname) {
                state.surname = action.profile.surname
            }
            if (action.profile.mail) {
                state.mail = action.profile.mail
            }
            if (action.profile.avatar) {
                if (action.profile.avatar.indexOf('.')<1) {
                    state.avatar = action.profile.avatar
                    state.avatar_optimize = action.profile.avatar
                } else {
                    state.avatar = action.profile.avatar
                    state.avatar_optimize = action.profile.avatar
                }
            }

            return state

        default:
            return {
                id: state.id || 0,
                login: state.login,
                avatar: state.avatar || '/user.png',
                avatar_optimize: state.avatar || '/user.png',
                name: state.name,
                surname: state.surname,
                phone: state.phone,
                mail: state.mail,
                social: state.social || [],
                admin: state.admin || 2,
            };
    }
}

export const reducers = combineReducers({
    system, online, profile, posts,
})

// store.js

const persistConfig = {
    key: 'primary',
    storage,
    // whitelist: ['exampleData'],
}

const persistedReducer = persistReducer(persistConfig, reducers)

function makeStore(initialState = {}) {
    return createStore(
        persistedReducer,
        initialState,
        composeWithDevTools(applyMiddleware())
    )
}

export const initializeStore = (preloadedState) => {
    let _store = store ?? makeStore(preloadedState)

    // After navigating to a page with an initial Redux state, merge that state
    // with the current state in the store, and create a new store
    if (preloadedState && store) {
        _store = makeStore({
            ...store.getState(),
            ...preloadedState,
        })
        // Reset the current store
        store = undefined
    }

    // For SSG and SSR always create a new store
    if (typeof window === 'undefined') return _store
    // Create the store once in the client
    if (!store) store = _store

    return _store
}

export function useStore(initialState) {
    const store = useMemo(() => initializeStore(initialState), [initialState])
    return store
}
