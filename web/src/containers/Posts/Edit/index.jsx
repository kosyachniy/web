import React, { useState } from 'react'
import { Redirect } from 'react-router-dom'
import { useTranslation } from 'react-i18next'

import api from '../../../lib/api'

import './style.css'
// import Editor from '../../../components/Editor'


const Edit = (props) => {
    const [title, setName] = useState(props.post ? props.post.title : '')
    const [data, setCont] = useState(props.post ? props.post.data : '')
    const [redirect, setRedirect] = useState(null)
    const { t } = useTranslation()

    const editPost = () => {
        let req = { title, data }

        if (props.post) {
            req['id'] = props.post.id
        }

        api('posts.save', req).then(res => {
            if (props.post) {
                props.handlerSave()
            } else {
                setRedirect(res.id)
            }
        })
    }

    if (redirect) {
        return (
            <Redirect to={`/post/${redirect}`} />
        )
    }

    return (
        <div id="edit">
            <div className="album py-5">
                <div className="input-group mb-3">
                    <input
                        type="text"
                        className="form-control name"
                        placeholder={ t('posts.title') }
                        value={ title }
                        onChange={ (event) => {setName(event.target.value)} }
                    />
                </div>

                {/* <Editor
                    data={ data }
                    updatePost={ (text) => {setCont(text)} }
                /> */}

                <br />
                <button
                    className="btn btn-success"
                    style={ {width: '100%'} }
                    onClick={ editPost }
                >
                    <i className="far fa-save" />
                </button>
            </div>
        </div>
    );
};

export default Edit;
