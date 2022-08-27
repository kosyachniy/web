import React, { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { withTranslation } from 'react-i18next'

import api from '../../../lib/api'

import './style.css'


const Feed = (props) => {
    const { t } = props

    const getPost = (data={}) => {
        api('posts.get', data).then(res => {
            props.postsGet(res['posts'])
        })
    }

    useEffect(() => {
        getPost()
    }, [])

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
            <div className="container" id="feed">
                <Link to="/post/add">
                    <button
                        type="button"
                        className="btn btn-success"
                        style={ {width: '100%'} }
                    >
                        <i className="fas fa-plus" />
                    </button>
                </Link>

                { !props.posts.length && (
                    <p>{ t('posts.empty') }!</p>
                ) }

                { props.posts.map(post => (
                    <div className="cards" key={ post.id }>
                        <Link to={ `/post/${post.id}` } >
                            <div className="cards-content">
                                <h3 className="title">{ post.title }</h3>
                                <div className="additional"><i className="fas fa-ellipsis-v" /></div>
                                <div className="time">{ getTime(post.time) }</div>
                            </div>
                            { post.cover && (
                                <img src={ post.cover } alt={ post.title } />
                            ) }
                            <div className="cards-content">
                                <div className="content short">{ post.data }</div>
                            </div>
                        </Link>
                        <div className="cards-content reactions">
                            <div><i className="far fa-heart" />{ post.reactions.likes ? " " + post.reactions.likes : "" }</div>
                            {/* <i className="fas fa-heart" /> */}
                            <div><i className="far fa-comment" /> { post.reactions.comments.length ? " " + post.reactions.comments.length : "" }</div>
                            <div><i className="fas fa-share" />{ post.reactions.reposts ? " " + post.reactions.reposts : "" }</div>
                        </div>
                    </div>
                )) }
            </div>
        </>
    )
}

export default withTranslation()(Feed);
