export default (state = {
    id: 0,
    login: null,
    name: null,
    surname: null,
    phone: null,
    mail: null,
    image: '/user.png',
    image_optimize: '/user.png',
    social: [],
    admin: 2,
}, action) => {
    switch (action.type) {
        case 'PROFILE_IN':
            return {
                id: action.id,
                login: action.login,
                name: action.name,
                surname: action.surname,
                phone: action.phone,
                mail: action.mail,
                image: action.image || '/user.png',
                image_optimize: action.image || '/user.png',
                admin: action.admin,
            }

        case 'PROFILE_OUT':
            return {
                id: 0,
                login: null,
                name: null,
                surname: null,
                phone: null,
                mail: null,
                image: null,
                image_optimize: null,
                admin: 2,
            }

        case 'PROFILE_UPDATE':
            if (action.profile.login) {
                state.login = action.profile.login
            }
            if (action.profile.name) {
                state.name = action.profile.name
            }
            if (action.profile.surname) {
                state.surname = action.profile.surname
            }
            if (action.profile.phone) {
                state.phone = action.profile.phone
            }
            if (action.profile.mail) {
                state.mail = action.profile.mail
            }
            if (action.profile.image) {
                if (action.profile.image.indexOf('.')<1) {
                    state.image = action.profile.v
                    state.image_optimize = action.profile.image
                } else {
                    state.image = action.profile.image
                    state.image_optimize = action.profile.image
                }
            }

            return state

        default:
            return state
    }
}
