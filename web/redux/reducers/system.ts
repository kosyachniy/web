import { AnyAction } from 'redux';

export default (state = {
  search: '',
  prepared: false,
  loaded: false,
  popup: null,
}, action: AnyAction) => {
  switch (action.type) {
    case 'SYSTEM_PREPARED':
      return {
        ...state,
        prepared: true,
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
      };

    default:
      return state;
  }
};
