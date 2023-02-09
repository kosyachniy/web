import { AnyAction } from 'redux';

export default (state = {
  id: 0,
  login: null,
  name: null,
  surname: null,
  title: null,
  phone: null,
  mail: null,
  image: '/user.png',
  image_optimize: '/user.png',
  social: [],
  status: 2,
}, action: AnyAction) => {
  switch (action.type) {
    case 'PROFILE_IN':
      return {
        id: action.id,
        login: action.login,
        name: action.name,
        surname: action.surname,
        title: action.title,
        phone: action.phone,
        mail: action.mail,
        image: action.image || '/user.png',
        image_optimize: action.image || '/user.png',
        status: action.status,
      };

    case 'PROFILE_OUT':
      return {
        id: 0,
        login: null,
        name: null,
        surname: null,
        title: null,
        phone: null,
        mail: null,
        image: null,
        image_optimize: null,
        status: 2,
      };

    case 'PROFILE_UPDATE':
      return {
        ...state,
        login: action.profile.login || state.login,
        name: action.profile.name || state.name,
        surname: action.profile.surname || state.surname,
        title: action.profile.title || state.title,
        phone: action.profile.phone || state.phone,
        mail: action.profile.mail || state.mail,
        image: action.profile.image || state.image,
        image_optimize: action.profile.image || state.image_optimize,
      };

    default:
      return state;
  }
};
