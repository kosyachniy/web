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
import { createWrapper } from 'next-redux-wrapper';

import reducer from './reducers/index.ts';

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
