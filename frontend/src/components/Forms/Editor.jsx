import { useEffect, useRef } from 'react';
import { useSelector } from 'react-redux';

import Loader from '../Loader';

export default ({ editorLoaded, data, updatePost }) => {
  const editorRef = useRef();
  const main = useSelector(state => state.main);
  const { CKEditor, ClassicEditor } = editorRef.current || {};

  useEffect(() => {
    editorRef.current = {
      CKEditor: require('@ckeditor/ckeditor5-react').CKEditor,
      ClassicEditor: require('@kosyachniy/ckeditor'),
    };
  }, []);

  return (
    <>
      { editorLoaded ? (
        <CKEditor
          editor={ClassicEditor}
          config={{
            simpleUpload: {
              uploadUrl: `${process.env.NEXT_PUBLIC_API}upload/`,
              // withCredentials: true,
              // headers: {
              //     'X-CSRF-TOKEN': 'CSRF-Token',
              //     Authorization: 'Bearer <JSON Web Token>'
              // }
            },
            mediaEmbed: {
              previewsInData: true,
            },
          }}
          data={data}
          onReady={editor => {
            editor.editing.view.change(writer => {
              writer.setStyle(
                'min-height',
                '400px',
                editor.editing.view.document.getRoot(),
              );
              writer.setStyle(
                'background-color',
                `rgba(var(--bs-${main.theme}-rgb), var(--bs-bg-opacity))!important;`,
                editor.editing.view.document.getRoot(),
              );
              writer.setStyle(
                'color',
                `rgba(var(--bs-${main.color}-rgb));`,
                editor.editing.view.document.getRoot(),
              );
            });
          }}
          onChange={(event, editor) => updatePost(editor.getData())}
        />
      ) : (<Loader />) }
    </>
  );
};
