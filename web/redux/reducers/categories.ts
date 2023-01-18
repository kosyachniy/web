import { AnyAction } from 'redux';

export default (state = null, action: AnyAction) => {
  switch (action.type) {
    case 'CATEGORIES_GET':
      if (action.categories) {
        return action.categories;
      }
      return state;

    case 'CATEGORIES_ADD':
      return [
        ...state,
        action.category,
      ];

    case 'CATEGORIES_CLEAR':
      return null;

    default:
      return state;
  }
};
