import { useEffect, useRef } from "react"


export default ({ editorLoaded, data, updatePost }) => {
    const editorRef = useRef()
    const { CKEditor, ClassicEditor } = editorRef.current || {}

    useEffect(() => {
        editorRef.current = {
            CKEditor: require("@ckeditor/ckeditor5-react").CKEditor,
            ClassicEditor: require("@kosyachniy/ckeditor"),
        }
    }, [])

    return (
        <>
            { editorLoaded ? (
                <CKEditor
                    editor={ ClassicEditor }
                    config={{
                        simpleUpload: {
                            uploadUrl: `${process.env.NEXT_PUBLIC_API}upload/`,
                            // withCredentials: true,
                            // headers: {
                            //     'X-CSRF-TOKEN': 'CSRF-Token',
                            //     Authorization: 'Bearer <JSON Web Token>'
                            // }
                        }
                    }}
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
