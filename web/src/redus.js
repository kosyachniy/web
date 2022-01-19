import i18n from './i18n'

import { combineReducers, createStore } from 'redux';


// actions.js
export const postsGet = posts => ({
    type: 'POSTS_GET',
    posts,
});

export const postsAdd = post => ({
    type: 'POSTS_ADD',
    post,
});

export const postsEdit = post => ({
    type: 'POSTS_EDIT',
    post,
});

export const postsDelete = id => ({
    type: 'POSTS_DELETE',
    id,
});

export const onlineAdd = online => ({
    type: 'ONLINE_ADD',
    count: online.count,
    users: online.users,
});

export const onlineDelete = online => ({
    type: 'ONLINE_DELETE',
    count: online.count,
    ids: online.users.map(user => user.id),
});

export const onlineReset = () => ({
    type: 'ONLINE_RESET',
});

export const changeTheme = theme => {
    localStorage.setItem('theme', theme)

    const color = theme === 'dark' ? 'light' : 'dark'
    localStorage.setItem('color', color)

    return {
        type: 'CHANGE_THEME',
        theme, color,
    }
}

export const searching = search => {
    localStorage.setItem('search', search)

    return {
        type: 'SEARCH',
        search,
    }
}

export const changeLang = locale => {
    localStorage.setItem('locale', locale)
    i18n.changeLanguage(locale)

    return {
        type: 'CHANGE_LANG',
        locale,
    }
}

export const profileIn = profile => {
    const { id, login, avatar, name, surname, phone, mail, social, status } = profile

    if (id) {
        localStorage.setItem('id', id)
    }
    if (login) {
        localStorage.setItem('login', login)
    }
    if (avatar) {
        localStorage.setItem('avatar', avatar)
    }
    if (name) {
        localStorage.setItem('name', name)
    }
    if (surname) {
        localStorage.setItem('surname', surname)
    }
    if (phone) {
        localStorage.setItem('phone', phone)
    }
    if (mail) {
        localStorage.setItem('mail', mail)
    }
    if (social) {
        localStorage.setItem('social', social)
    }
    if (status) {
        localStorage.setItem('status', status)
    }

    return {
        type: 'PROFILE_IN',
        id, login, avatar, name, surname, phone, mail, social, status,
    }
};

export const profileOut = () => {
    localStorage.removeItem('id')
    localStorage.removeItem('login')
    localStorage.removeItem('avatar')
    localStorage.removeItem('name')
    localStorage.removeItem('surname')
    localStorage.removeItem('phone')
    localStorage.removeItem('mail')
    localStorage.removeItem('social')
    localStorage.removeItem('status')

    return {
        type: 'PROFILE_OUT',
    }
};

export const profileUpdate = profile => {
    ['login', 'avatar', 'name', 'surname', 'phone', 'mail', 'social', 'status'].map(el => {
        if (el in profile && profile[el]) {
            localStorage.setItem(el, profile[el])
        }

        return null;
    })

    return {
        type: 'PROFILE_UPDATE',
        profile,
    }
};

export const systemLoaded = () => ({
    type: 'SYSTEM_LOADED',
});

// reducers.js
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
};

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
};

export const system = (state = {
    loaded: false,
    locale: localStorage.getItem('locale'),
    theme: localStorage.getItem('theme'),
    color: localStorage.getItem('color'),
    search: localStorage.getItem('search'),
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

        case 'SEARCH':
            return {
                ...state,
                search: action.search,
            }

        default:
            return {
                loaded: state.loaded,
                locale: state.locale || process.env.REACT_APP_LOCALE,
                theme: state.theme || 'light',
                color: state.color || 'dark',
                search: state.search || '',
            };
    }
};

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
                id: state.id || localStorage.getItem('id') || 0,
                login: state.login || localStorage.getItem('login'),
                avatar: state.avatar || localStorage.getItem('avatar') || '/user.png',
                avatar_optimize: state.avatar || localStorage.getItem('avatar') || '/user.png',
                name: state.name || localStorage.getItem('name'),
                surname: state.surname || localStorage.getItem('surname'),
                phone: state.phone || localStorage.getItem('phone'),
                mail: state.mail || localStorage.getItem('mail'),
                social: state.social || localStorage.getItem('social') || [],
                admin: state.admin || localStorage.getItem('admin') || 2,
            };
    }
};

export const reducers = combineReducers({
    system, online, profile, posts,
});

// store.js
export function configureStore(initialState = {}) {
    const store = createStore(reducers, initialState);
    return store;
}

export const store = configureStore();
