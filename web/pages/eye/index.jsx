import { useState, useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { useRouter } from 'next/router'
import { useTranslation } from 'next-i18next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'

import api from '../../lib/api'


export default () => {
    const { t } = useTranslation('common')
    const router = useRouter()
    const dispatch = useDispatch()
    const system = useSelector((state) => state.system)
    const main = useSelector((state) => state.main)
    const profile = useSelector((state) => state.profile)
    const [categories, setCategories] = useState([])

    useEffect(() => {
        if (system.prepared) {
            // TODO: categories
        }
    }, [system.prepared])

    if (profile.status < 6) {
        router.push(`/`)
    }

    return (
        <>
            <h1>{ t('system.admin') }</h1>
            { categories.map(category => (
                <div>
                    { category }
                </div>
            )) }
        </>
    )
}

export const getStaticProps = async ({ locale }) => ({
    props: {
        ...await serverSideTranslations(locale, ['common']),
    },
})
