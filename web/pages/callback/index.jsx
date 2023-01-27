import { useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { useRouter } from 'next/router'
import { useTranslation } from 'next-i18next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'

import { popupSet, toastAdd } from '../../redux/actions/system'
import { profileIn } from '../../redux/actions/profile'
import api from '../../lib/api'


export default () => {
    const { t } = useTranslation('common')
    const dispatch = useDispatch()
    const router = useRouter()
    const main = useSelector(state => state.main)
    const previousPath = localStorage.getItem('previousPath')

    const onSocial = (type, code) => api(main, 'account.social', {
        social: type,
        code,
        utm: main.utm,
    }).then(res => {
        dispatch(profileIn(res))
        dispatch(popupSet(null))
        router.push(previousPath)
    }).catch(err => dispatch(toastAdd({
        header: t('system.error'),
        text: err,
        color: 'white',
        background: 'danger',
    })))

    useEffect(() => {
        const params = Object.fromEntries(new URLSearchParams(document.location.search))
        if (params.code) {
            const code = params.code
            if (code === undefined) {
                router.push("/")
            }

            let type
            if (document.location.search.indexOf('google') !== -1) {
                type = 'g'
            } else if (document.location.search.indexOf('telegram') !== -1) {
                type = 'tg'
            } else if (document.location.search.indexOf('state=fb') !== -1) {
                type = 'fb'
            } else {
                type = 'vk'
            }

            onSocial(type, code)
        } else {
            router.push("/")
        }
    }, [])

    return (
        <></>
    )
}

export const getStaticProps = async ({ locale }) => {
    return {
        props: {
            ...await serverSideTranslations(locale, ['common']),
        },
    }
}
