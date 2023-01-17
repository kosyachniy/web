import { configureStore } from "@reduxjs/toolkit"
import {
    persistStore, persistReducer,
    FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER,
} from "redux-persist"
import storage from "redux-persist/lib/storage"

import reducer from "./reducers"


export default () => {
    const store = configureStore({
        reducer: persistReducer({
            key: 'root',
            storage,
            whitelist: ['main', 'profile'],
        }, reducer),
        middleware: getDefaultMiddleware => getDefaultMiddleware({
            serializableCheck: {
                ignoredActions: [
                    FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER,
                ],
            },
        }),
    })

    const persistor = persistStore(store)
    return { store, persistor }
}
