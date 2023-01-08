import { useEffect, useRef } from "react"


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
                    editor={ ClassicEditor }
                    data={ data }
                    onReady={ (editor) => {
                        editor.editing.view.change((writer) => {
                            writer.setStyle(
                                'min-height',
                                '400px',
                                editor.editing.view.document.getRoot()
                            )
                        })
                    } }
                    onChange={ (event, editor) => {
                        updatePost(editor.getData())
                    } }
                    // onBlur={ (event, editor) => {
                    //     console.log( 'Blur.', editor )
                    // } }
                    // onFocus={ (event, editor) => {
                    //     console.log( 'Focus.', editor )
                    // } }
                />
            ) : (<>Editor loading</>) }
        </>
    )
}
