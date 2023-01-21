import { AnyAction } from 'redux';

export default (state = {
  search: '',
  prepared: false,
  popup: null,
  toasts: [],
}, action: AnyAction) => {
  switch (action.type) {
    case 'SYSTEM_PREPARED':
      return {
        ...state,
        prepared: true,
      };

    case 'SYSTEM_POPUP':
      return {
        ...state,
        popup: action.popup,
      };

    case 'SYSTEM_TOAST':
      return {
        ...state,
        toasts: [ ...state.toasts, action.toast ],
      };

    case 'SEARCH':
      return {
        ...state,
        search: action.search,
      };

    default:
      return state;
  }
};
