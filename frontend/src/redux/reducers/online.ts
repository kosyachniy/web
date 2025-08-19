import { AnyAction } from 'redux';

export default (state = {
  count: null,
  users: [],
}, action: AnyAction) => {
  switch (action.type) {
    case 'ONLINE_ADD':
      return {
        count: action.count,
        users: [
          ...action.users,
          ...state.users,
        ],
      };

    case 'ONLINE_DELETE':
      return {
        count: action.count,
        users: state.users.filter((user) => action.ids.indexOf(user.id) === -1),
      };

    case 'ONLINE_RESET':
      return {
        count: null,
        users: [],
      };

    default:
      return state;
  }
};
