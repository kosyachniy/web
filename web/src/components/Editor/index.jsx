import React from 'react'

import CKEditor from '@ckeditor/ckeditor5-react'
import ClassicEditor from '@kosyachniy/ckeditor'

import './style.css'


export default class Editor extends React.Component {
    render() {
        return (
            <CKEditor
                editor={ ClassicEditor }
                data={ this.props.data }
                // onReady={ editor => {
                //     // You can store the "editor" and use when it is needed.
                //     console.log( 'Editor is ready to use!', editor );
                // } }
                onChange={ (event, editor) => {
                    this.props.updatePost(editor.getData())
                } }
                // onBlur={ ( event, editor ) => {
                //     console.log( 'Blur.', editor );
                // } }
                // onFocus={ ( event, editor ) => {
                //     console.log( 'Focus.', editor );
                // } }
            />
        )
    }
}
