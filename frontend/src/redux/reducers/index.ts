import { combineReducers } from '@reduxjs/toolkit';

import system from './system';
import main from './main';
import profile from './profile';
import online from './online';
import categories from './categories';


export default combineReducers({
  system, main, profile, online, categories,
});
