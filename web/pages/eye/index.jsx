import { useState, useEffect } from 'react'
import { useSelector } from 'react-redux'
import { useRouter } from 'next/router'
import { useTranslation } from 'next-i18next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'

import api from '../../lib/api'


export default () => {
    const { t } = useTranslation('common')
    const router = useRouter()
    const system = useSelector((state) => state.system)
    const main = useSelector((state) => state.main)
    const profile = useSelector((state) => state.profile)
    const [categories, setCategories] = useState([])

    useEffect(() => {
        if (system.prepared) {
            api(main, 'categories.get').then(res => {
                if (res.categories) {
                    setCategories(res.categories)
                }
            })
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
                    { JSON.stringify(category) }
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
