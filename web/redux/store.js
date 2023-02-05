import { configureStore } from '@reduxjs/toolkit';
import {
  persistStore,
  persistReducer,
  FLUSH,
  REHYDRATE,
  PAUSE,
  PERSIST,
  PURGE,
  REGISTER,
} from 'redux-persist';
import storage from 'redux-persist/lib/storage';
import { HYDRATE, createWrapper } from 'next-redux-wrapper';

import combinedReducer from './reducers/index.ts';

const reducer = (state, action) => {
  if (action.type === HYDRATE) {
    const nextState = {
      ...state,
      ...action.payload,
    };
    return nextState;
  }
  return combinedReducer(state, action);
};

export default createWrapper(() => {
  const store = configureStore({
    reducer: persistReducer(
      {
        key: 'root',
        storage,
        whitelist: ['main', 'profile'],
      },
      reducer,
    ),
    middleware: (getDefaultMiddleware) => getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      },
    }),
  });
  store.__persistor = persistStore(store); /* eslint-disable-line */
  return store;
});
