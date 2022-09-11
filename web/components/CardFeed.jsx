import { useTranslation } from 'next-i18next'
import Link from 'next/link'

import styles from '../styles/feed.module.css'


export default ({ posts }) => {
    const { t } = useTranslation('common')

    const getTime = (time) => {
        const newTime = new Date(time * 1000);

        const year = newTime.getFullYear();
        let day = `${newTime.getDate()}`;
        let hours = `${newTime.getHours()}`;
        let minutes = `${newTime.getUTCMinutes()}`;

        let month = [
            'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
            'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря',
        ][newTime.getMonth()];

        if (day.length < 2) {
            day = `0${day}`
        }

        if (hours.length < 2) {
            hours = `0${hours}`
        }

        if (minutes.length < 2) {
            minutes = `0${minutes}`
        }

        return `${day} ${month} ${year} в ${hours}:${minutes}`;
    }

    return (
        <>
            <div className={ `container ${styles.feed}` }>
                <Link href="/posts/add">
                    <button
                        type="button"
                        className="btn btn-success"
                        style={{ width: '100%' }}
                    >
                        <i className="fas fa-plus" />
                    </button>
                </Link>

                { !posts.length && (
                    <p>{ t('posts.empty') }!</p>
                ) }

                { posts.map(post => (
                    <div className={ styles.cards } key={ post.id }>
                        <Link href={ `/posts/${post.id}` } >
                            <>
                                <div className="cards-content">
                                    <h3 className={ styles.title }>{ post.title }</h3>
                                    <div className={ styles.additional }><i className="fas fa-ellipsis-v" /></div>
                                    <div className={ styles.time }>{ getTime(post.created) }</div>
                                </div>
                                { post.cover && (
                                    <img src={ post.cover } alt={ post.title } />
                                ) }
                                <div className="cards-content">
                                    <div className={ `${styles.content} ${styles.short}` }>{ post.data }</div>
                                </div>
                            </>
                        </Link>
                        <div className={ `cards-content ${styles.reactions}` }>
                            <div><i className="far fa-heart" />{ post.reactions.likes ? " " + post.reactions.likes : "" }</div>
                            {/* <i className="fas fa-heart" /> */}
                            <div><i className="far fa-comment" /> { post.reactions.comments.length ? " " + post.reactions.comments.length : "" }</div>
                            <div><i className="far fa-share" />{ post.reactions.reposts ? " " + post.reactions.reposts : "" }</div>
                        </div>
                    </div>
                )) }
            </div>
        </>
    )
}
