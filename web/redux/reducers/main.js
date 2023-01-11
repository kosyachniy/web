import { generate } from '../../lib/generate'


export default (state = {
    token: generate(),
    locale: process.env.NEXT_PUBLIC_LOCALE,
    theme: 'light',
    color: 'dark',
    display: 'grid',
}, action) => {
    switch (action.type) {
        case 'CHANGE_THEME':
            return {
                ...state,
                theme: action.theme,
                color: action.color,
            }

        case 'CHANGE_LANG':
            return {
                ...state,
                locale: action.locale,
            }

        case 'SYSTEM_DISPLAY':
            return {
                ...state,
                display: action.display,
            }

        default:
            return state
    }
}
