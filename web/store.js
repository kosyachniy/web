import {
    configureStore, combineReducers,
} from "@reduxjs/toolkit";
import {
    persistStore, persistReducer,
    FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER,
} from "redux-persist";
import storage from "redux-persist/lib/storage";
import { createOffline } from "@redux-offline/redux-offline";
import offlineConfig from "@redux-offline/redux-offline/lib/defaults";

import { generate } from './functions/generate'


const {
    middleware: offlineMiddleware,
    enhanceReducer: offlineEnhanceReducer,
    enhanceStore: offlineEnhanceStore,
} = createOffline({
    ...offlineConfig,
    persist: undefined,
    // ...customOfflineConfig,
});


// import { api } from "service/http";

// const effect = (effect, action) => {
//     let draft = effect;
//     if (action?.payload !== undefined && action?.payload !== null) {
//       draft = {
//         data: action.payload,
//         ...draft,
//       };
//     }
//     return api.request(draft);
// };
// const discard = (error, _action, _retries) => {
//     const status = error?.status || error?.response?.status || 503;
//     return 400 <= status && status < 500;
// };
// const customOfflineConfig = { effect, discard };


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

export const profileIn = ({ id, login, image, name, surname, phone, mail, social, status }) => ({
    type: 'PROFILE_IN',
    id, login, image, name, surname, phone, mail, social, status,
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

export const displaySet = display => ({
    type: 'SYSTEM_DISPLAY',
    display,
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
    display: 'grid',
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

        case 'SYSTEM_DISPLAY':
            return {
                ...state,
                display: action.display,
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
                display: state.display || 'grid',
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
    phone: null,
    mail: null,
    image: null,
    image_optimize: null,
    admin: 2,
}, action) => {
    switch (action.type) {
        case 'PROFILE_IN':
            return {
                id: action.id,
                login: action.login,
                name: action.name,
                surname: action.surname,
                phone: action.phone,
                mail: action.mail,
                image: action.image || '/user.png',
                image_optimize: action.image || '/user.png',
                admin: action.admin,
            };

        case 'PROFILE_OUT':
            return {
                id: 0,
                login: null,
                name: null,
                surname: null,
                phone: null,
                mail: null,
                image: null,
                image_optimize: null,
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
            if (action.profile.phone) {
                state.phone = action.profile.phone
            }
            if (action.profile.mail) {
                state.mail = action.profile.mail
            }
            if (action.profile.image) {
                if (action.profile.image.indexOf('.')<1) {
                    state.image = action.profile.v
                    state.image_optimize = action.profile.image
                } else {
                    state.image = action.profile.image
                    state.image_optimize = action.profile.image
                }
            }

            return state

        default:
            return {
                id: state.id || 0,
                login: state.login,
                image: state.image || '/user.png',
                image_optimize: state.image || '/user.png',
                name: state.name,
                surname: state.surname,
                phone: state.phone,
                mail: state.mail,
                social: state.social || [],
                admin: state.admin || 2,
            };
    }
}


const persistConfig = {
    key: "root",
    version: 1,
    storage,
    // whitelist: ['system'],
}

export function makeStore() {
    const rootReducer = combineReducers({
        system, online, profile, posts,
    });
    const persistedReducer = persistReducer(
        persistConfig,
        offlineEnhanceReducer(rootReducer),
    );

    return configureStore({
        reducer: persistedReducer,
        enhancers: [offlineEnhanceStore],
        middleware: (getDefaultMiddleware) => getDefaultMiddleware({
            serializableCheck: {
                ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
            },
        }).concat(offlineMiddleware),
    });
}

const store = makeStore();
export const persistor = persistStore(store);
export default store;
