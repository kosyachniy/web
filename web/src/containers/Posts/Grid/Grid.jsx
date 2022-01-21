import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { withTranslation } from 'react-i18next'

import api from '../../../lib/api'

import Card from '../../../components/Card'


const Grid = (props) => {
    const {
        system, posts,
        postsGet,
    } = props

    const [loaded, setLoaded] = useState(null)

    const getPost = (data={}) => {
        api('posts.get', data).then(res => {
            postsGet(res['posts'])
        })
    }

    useEffect(() => {
        if (
            system.search !== loaded
            && (
                system.search === ''
                || system.search.length >= 3
            )
        ) {
            setLoaded(system.search)
            getPost({search: system.search})
        }
    })

    return (
        <>
            <div className="row">
                <div className="col-xs-10 col-sm-10 col-md-10">
                    <div className="btn-group" role="group" >
                        <button
                            type="button"
                            className={`btn btn-${system.theme}`}
                        >
                            <i className="fas fa-th-large"></i>
                        </button>
                        <button
                            type="button"
                            className={`btn btn-${system.theme}`}
                        >
                            <i className="fas fa-th-list"></i>
                        </button>
                        <button
                            type="button"
                            className={`btn btn-${system.theme}`}
                        >
                            <i className="fas fa-image"></i>
                        </button>
                    </div>
                </div>
                <div className="col-xs-2 col-sm-2 col-md-2" style={ {textAlign: 'right'} }>
                    <div className="btn-group">
                        <Link to="/post/add">
                            <button
                                type="button"
                                className="btn btn-success"
                                style={ {width: '100%'} }
                            >
                                <i className="fas fa-plus" />
                            </button>
                        </Link>
                    </div>
                </div>
            </div>

            <div className="album py-2">
                <div className="row">
                    { posts.map((el, num) =>
                        <Card post={ el } key={ num } />
                    ) }
                </div>
            </div>
        </>
    )
}

export default withTranslation()(Grid);
