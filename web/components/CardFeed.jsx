import Link from 'next/link'
import { useTranslation } from 'next-i18next'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

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
                        <FontAwesomeIcon icon="fa-solid fa-plus" />
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
                                    <div className={ styles.additional }><FontAwesomeIcon icon="fa-solid fa-ellipsis-vertical" /></div>
                                    <div className={ styles.time }>{ getTime(post.created) }</div>
                                </div>
                                { post.image && (
                                    <img src={ post.image } alt={ post.title } />
                                ) }
                                <div className="cards-content">
                                    <div className={ `${styles.content} ${styles.short}` }>{ post.data }</div>
                                </div>
                            </>
                        </Link>
                        <div className={ `cards-content ${styles.reactions}` }>
                            <div><FontAwesomeIcon icon="fa-regular fa-heart" />{ post.reactions.likes ? " " + post.reactions.likes : "" }</div>
                            {/* <FontAwesomeIcon icon="fa-solid fa-heart" /> */}
                            <div><FontAwesomeIcon icon="fa-regular fa-comment" /> { post.reactions.comments.length ? " " + post.reactions.comments.length : "" }</div>
                            <div><FontAwesomeIcon icon="fa-solid fa-share" />{ post.reactions.reposts ? " " + post.reactions.reposts : "" }</div>
                        </div>
                    </div>
                )) }
            </div>
        </>
    )
}
