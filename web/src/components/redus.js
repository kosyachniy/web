import { combineReducers, createStore } from 'redux';

// actions.js
export const postsGet = posts => ({
	type: 'POSTS_GET',
	posts,
});

export const postsAdd = note => ({
	type: 'POSTS_ADD',
	note,
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

export const changeTheme = theme => ({
	type: 'CHANGE_THEME',
	theme,
});

// reducers.js
export const posts = (state = [], action) => {
	switch (action.type) {
		case 'POSTS_GET':
			return action.posts;

		case 'POSTS_ADD':
			return [
				action.note,
				...state
			];

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

export const system = (state = {theme: 'light', color: 'dark'}, action) => {
	switch (action.type) {
		case 'CHANGE_THEME':
			return {
				theme: action.theme,
				color: action.theme === 'dark' ? 'light' : 'dark',
			};

		default:
			return state;
	}
};

export const reducers = combineReducers({
	system, posts, online,
});

// store.js
export function configureStore(initialState = {}) {
	const store = createStore(reducers, initialState);
	return store;
}

export const store = configureStore();
