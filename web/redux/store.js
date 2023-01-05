import { configureStore } from "@reduxjs/toolkit";
import {
    persistStore, persistReducer,
    FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER,
} from "redux-persist";
import storage from "redux-persist/lib/storage";
import { createOffline } from "@redux-offline/redux-offline";
import offlineConfig from "@redux-offline/redux-offline/lib/defaults";

import reducer from './reducers'


const {
    middleware: offlineMiddleware,
    enhanceReducer: offlineEnhanceReducer,
    enhanceStore: offlineEnhanceStore,
} = createOffline({
    ...offlineConfig,
    persist: undefined,
    // ...customOfflineConfig,
});


export function makeStore() {
    const persistedReducer = persistReducer({
        key: "root",
        version: 1,
        storage,
        // whitelist: ['system'],
    }, offlineEnhanceReducer(reducer));

    return configureStore({
        reducer: persistedReducer,
        enhancers: [offlineEnhanceStore],
        middleware: (getDefaultMiddleware) => getDefaultMiddleware({
            serializableCheck: {
                ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
            },
        }).concat(offlineMiddleware),
    });
}

const store = makeStore();
export const persistor = persistStore(store);
export default store;
