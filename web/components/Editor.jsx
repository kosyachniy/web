import { useEffect, useRef } from "react"

import styles from '../styles/editor.module.css'


export default ({ editorLoaded, data, updatePost }) => {
    const editorRef = useRef()
    const { CKEditor, ClassicEditor } = editorRef.current || {}

    useEffect(() => {
        editorRef.current = {
            CKEditor: require("@ckeditor/ckeditor5-react").CKEditor,
            ClassicEditor: require("@ckeditor/ckeditor5-build-classic")
        }
    }, [])

    return (
        <>
            { editorLoaded ? (
                <CKEditor
                    className={ styles.editor }
                    editor={ ClassicEditor }
                    data={ data }
                    // onReady={ editor => {
                    //     // You can store the "editor" and use when it is needed.
                    //     console.log( 'Editor is ready to use!', editor )
                    // } }
                    onChange={ ( event, editor ) => {
                        updatePost(editor.getData())
                    } }
                    // onBlur={ ( event, editor ) => {
                    //     console.log( 'Blur.', editor )
                    // } }
                    // onFocus={ ( event, editor ) => {
                    //     console.log( 'Focus.', editor )
                    // } }
                />
            ) : (<>Editor loading</>) }
        </>
    )
}
