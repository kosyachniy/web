import { AnyAction } from 'redux';

export default (state = {
  token: null,
  locale: process.env.NEXT_PUBLIC_LOCALE,
  theme: 'light',
  color: 'dark',
  display: 'grid',
  utm: null,
}, action: AnyAction) => {
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

    case 'SYSTEM_DISPLAY':
      return {
        ...state,
        display: action.display,
      };

    case 'SET_TOKEN':
      return {
        ...state,
        token: action.token,
      };

    case 'SET_UTM':
      return {
        ...state,
        utm: action.utm,
      };

    default:
      return state;
  }
};
