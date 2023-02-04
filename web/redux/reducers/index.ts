import { combineReducers } from '@reduxjs/toolkit';

import system from './system';
import main from './main';
import profile from './profile';
import online from './online';
import categories from './categories';


// import {AnyAction} from 'redux';
// import {HYDRATE} from 'next-redux-wrapper';

// export interface State {
//   tick: string;
// }

// const extra = (state: State = {tick: 'init'}, action: AnyAction) => {
//   switch (action.type) {
//     case HYDRATE:
//       return {...state, ...action.payload};
//     case 'TICK':
//       return {...state, tick: action.payload};
//     default:
//       return state;
//   }
// };

export default combineReducers({
  system, main, profile, online, categories, // extra,
});
