import { useSelector } from 'react-redux'

import api from '../../lib/api'
import Loader from '../../components/Loader'


export default ({ user, onPopup, onRedirect, onUpdateUserProperties }) => {
    const main = useSelector((state) => state.main)

    const onSocial = (type, code) => {
        api(main, 'account.social', {
            social: type,
            code,
            // TODO: utm
        }).then((_eventAuthSocialAccount) => {
            if (_eventAuthSocialAccount.id !== undefined) {
                onPopup(false)

                onUpdateUserProperties(_eventAuthSocialAccount, _eventAuthSocialAccount.new)

                if (!_eventAuthSocialAccount.new) {
                    localStorage.setItem('auth', true)
                }

                onRedirect(localStorage.getItem('previousPath').split('tensy.org')[1])
            } else {
                onRedirect(localStorage.getItem('previousPath').split('tensy.org')[1])
            }
        }).catch(() => {
            onRedirect(localStorage.getItem('previousPath').split('tensy.org')[1])
        })
    }

    useEffect(() => {
		if (user.id === undefined || (user.id !== undefined && user.id === 0)) {
			onRedirect('/')
		}

		const code = document.location.search.split('&')[0].split('=')[1]

		if (code === undefined) {
			onRedirect('/')
		}

		let type
		if (document.location.search.indexOf('google') !== -1) {
			type = 'g'
		} else if (document.location.search.indexOf('state=fb') !== -1) {
			type = 'fb'
		} else {
			type = 'vk'
		}

		onSocial(type, code)
    }, [])

    return (
        <div className="module">
            <Loader />
        </div>
    )
}
