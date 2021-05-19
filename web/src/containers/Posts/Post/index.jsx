import React, { useState, useEffect } from 'react'
import { Redirect } from 'react-router-dom'
// import ReactHtmlParser from 'react-html-parser'
import MathJax from 'react-mathjax-preview'

import api from '../../../func/api'

import './style.css'
import Edit from '../Edit'
// import Map from '../../../components/Map'


const Post = () => {
    const [post, setPost] = useState(null)
    const [edit, setEdit] = useState(false)
    const [deleted, setDeleted] = useState(false)

    const getPost = (data={}) => {
        const handlerSuccess = (res) => {
            setPost(res['posts'][0])
        }

        api('posts.get', data, handlerSuccess)
    }

    const savePost = () => {
        getPost({ id: post.id })
        setEdit(false)
    }

    const deletePost = () => {
        const data = {
            id: post.id,
        }

        const handlerSuccess = (res) => {
            setDeleted(true)
        }

        api('posts.delete', data, handlerSuccess)
    }

    useEffect(() => { // WillMount
        let postID = Number(document.location.pathname.split('/').pop())
        getPost({id: postID})
    }, [])

    if (deleted) {
        return (
            <Redirect to="/" />
        )
    }

    if (!post) {
        return (
            <></>
        )
    }

    return (
        <div id="post">
            <div className="album py-2">
                <h1>{ post.name }</h1>

                { edit ? (
                    <button
                        className="btn btn-outline-secondary"
                        onClick={ () => {setEdit(false)} }
                    >
                        <i className="far fa-eye" />
                    </button>
                ) : (
                    <button
                        className="btn btn-outline-secondary"
                        onClick={ () => {setEdit(true)} }
                    >
                        <i className="far fa-edit" />
                    </button>
                ) }
                <button
                    className="btn btn-danger"
                    onClick={ deletePost }
                >
                    <i className="far fa-trash-alt" />
                </button>

                { edit ? (
                    <Edit
                        post={ post }
                        handlerSave={ savePost }
                    />
                ) : (
                    <>
                        {/* <img src={ post.cover } alt={ post.name } /> */}
                        <br /><br />
                        <MathJax math={ post.cont } />

                        {/* <div style={{ marginTop: '50px', height: '250px' }}>
                            { post.geo ? (
                                <Map center={ post.geo} zoom={ 14 } />
                            ) : (
                                <Map />
                            )}
                        </div> */}
                    </>
                ) }
            </div>
        </div>
    )
}

export default Post;
