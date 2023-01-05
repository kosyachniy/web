export default (state = {
    search: '',
    loaded: false,
    popup: null,
}, action) => {
    switch (action.type) {
        case 'SYSTEM_LOADED':
            return {
                ...state,
                loaded: true,
            }

        case 'SYSTEM_POPUP':
            return {
                ...state,
                popup: action.popup,
            }

        case 'SEARCH':
            return {
                ...state,
                search: action.search,
            }

        default:
            return state
    }
}
