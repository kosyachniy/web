import { useState, useEffect } from 'react'
import { useSelector } from 'react-redux'
import { useRouter } from 'next/router'
import { useTranslation } from 'next-i18next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import api from '../../lib/api'
import Category from '../../components/Category'


export default () => {
    const { t } = useTranslation('common')
    const router = useRouter()
    const system = useSelector((state) => state.system)
    const main = useSelector((state) => state.main)
    const profile = useSelector((state) => state.profile)
    const [categories, setCategories] = useState([])
    const [edit, setEdit] = useState(null)

    const addCategory = () => {
        setCategories([...categories, { id: 0, title: '', data: null, parent: null }])
        setEdit(0)
    }

    useEffect(() => {
        if (system.prepared && !categories.length) {
            api(main, 'categories.get').then(res => {
                if (res.categories) {
                    setCategories(res.categories)
                }
            })
        }
    }, [system.prepared, categories])

    if (profile.status < 6) {
        router.push(`/`)
    }

    return (
        <>
            <h1>{ t('system.categories') }</h1>
            { categories.map(category => (
                <Category
                    category={ category }
                    edit={ edit === category.id }
                    setEdit={ setEdit }
                    categories={ categories }
                    setCategories={ setCategories }
                    key={ category.id }
                />
            )) }
            { edit !== 0 && (
                <button
                    type="button"
                    className="btn btn-success"
                    style={{ width: '100%' }}
                    onClick={ addCategory }
                >
                    <FontAwesomeIcon icon="fa-solid fa-plus" />
                </button>
            ) }
        </>
    )
}

export const getStaticProps = async ({ locale }) => ({
    props: {
        ...await serverSideTranslations(locale, ['common']),
    },
})
