import React, { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { withTranslation } from 'react-i18next'

import api from '../../../func/api'

import Card from '../../../components/Card'


const Grid = (props) => {
    // const { t } = props

    const getPost = (data={}) => {
        const handlerSuccess = (res) => {
            props.postsGet(res['posts']);
        }

        api('posts.get', data, handlerSuccess)
    }

    useEffect(() => {
        getPost()
    }, [])

    return (
        <>
            <div className="row">
                <div className="col-xs-10 col-sm-10 col-md-10">
                    <div className="btn-group">
                        <button type="button" className="btn btn-default"><i className="fas fa-th-large"></i></button>
                        <button type="button" className="btn btn-default"><i className="fas fa-th-list"></i></button>
                        <button type="button" className="btn btn-default"><i className="fas fa-image"></i></button>
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
                    { props.posts.map((el, num) =>
                        <Card post={ el } key={ num } />
                    ) }
                </div>
            </div>
        </>
    )
}

export default withTranslation()(Grid);
