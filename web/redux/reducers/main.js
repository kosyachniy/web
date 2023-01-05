import { generate } from '../../functions/generate'


export default (state = {
    token: generate(),
    locale: 'en',
    theme: null,
    color: null,
    display: 'grid',
}, action) => {
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

        default:
            return {
                token: state.token || generate(),
                locale: state.locale || process.env.NEXT_PUBLIC_LOCALE,
                theme: state.theme || 'light',
                color: state.color || 'dark',
                display: state.display || 'grid',
            };
    }
}
