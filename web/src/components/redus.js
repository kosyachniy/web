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

export const reducers = combineReducers({
	posts,
});

// store.js
export function configureStore(initialState = {}) {
	const store = createStore(reducers, initialState);
	return store;
}

export const store = configureStore();
