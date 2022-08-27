import React from 'react'
import { Link } from 'react-router-dom'

import './style.css'


const Card = (props) => {
    const { post } = props;

    return (
        <div className="col-md-4">
            <Link to={`/post/${post.id}`} key={ post.id }>
                <div className="card mb-4 shadow-sm">
                    { post.cover && <img className="card-img-top" src={ post.cover } alt={ post.title } /> }
                    <div className="card-body">
                        <p className="card-text">
                            {/* <span className="badge badge-success" style={ marginRight: '10px', fontSize: '15px' }>
                                <img src="/static/icon/{{ icon }}.svg">
                            </span> */}
                            { post.title }
                        </p>

                        { post.description && (
                            <div className="d-flex justify-content-between align-items-center">
                                { post.description }
                                {/* <div className="btn-group">
                                    <button type="button" className="btn btn-sm btn-outline-secondary">View</button>
                                    <button type="button" className="btn btn-sm btn-outline-secondary">Edit</button>
                                </div> */}
                                { post.additionally && <small className="text-muted">{ post.additionally }</small> }
                            </div>
                        ) }
                    </div>
                </div>
            </Link>
        </div>
    )
};

export default Card;
