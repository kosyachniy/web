import { useState, useEffect } from 'react'

import styles from '../styles/base.module.css'


const dataFilters = [
    'currencies',
    'crypto',
    'stocks',
    'commodities',
    'etfs',
    'funds',
    'bonds',
]
const dataCards = [
    {'title': 'Sunrise', 'image': 'https://farm6.staticflickr.com/5607/15374495498_db6e120f6c_b.jpg'},
    {'title': 'Sunset', 'image': 'https://proprikol.ru/wp-content/uploads/2020/09/kartinki-los-andzheles-45.jpg'},
    {'title': 'Darkness', 'image': 'https://pibig.info/uploads/posts/2021-12/1639642159_79-pibig-info-p-nochnie-gori-priroda-krasivo-foto-87.jpg'},
]


export default () => {
    const [data, setData] = useState(null)
    const [filters, setFilters] = useState(Object.fromEntries(dataFilters.map((f) => [f, false])))

    useEffect(() => {
        let token = localStorage.getItem('token')
        if (!token) {
            let symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'.split('')
            let token_raw = []
            for (let i=0; i<32; i++) {
                let j = (Math.random() * (symbols.length-1)).toFixed(0)
                token_raw[i] = symbols[j]
            }
            token = token_raw.join('')
            localStorage.setItem('token', token)
        }

        fetch(process.env.NEXT_PUBLIC_SERVER, {
            method: 'POST',
            body: JSON.stringify({ token }),
            headers: { 'Content-Type': 'application/json' },
        }).then(
            async res => setData(await res.json())
        )
    }, [])

    return (
        <>
            <input className={ styles.search } placeholder="🔍 Search" />
            <div className={ styles.filters }>
                { Object.entries(filters).map(([k, v]) => (
                    <button
                        className={ v ? styles.active : "" }
                        key={ k }
                        onClick={
                            () => {setFilters({
                                ...filters,
                                [k]: !v,
                            })}
                        }
                    >{ k }</button>
                )) }
            </div>
            <div className={ styles.cards }>
                { dataCards.map((v, k) =>
                    <div
                        key={ k }
                        style={{ backgroundImage: `url(${v.image})` }}
                    >
                        { v.title }
                    </div>
                ) }
            </div>
            <div className={ styles.box }>
                { data ? (
                    <div>
                        User #{ data.id }<br />
                        { JSON.stringify(data.token) }
                    </div>
                ) : 'Loading..' }
            </div>
            <button className={ styles.button }>
                Go
            </button>
        </>
    )
}
