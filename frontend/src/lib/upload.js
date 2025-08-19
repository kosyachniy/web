export default function upload(file) {
  return new Promise((resolve) => {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', `${process.env.NEXT_PUBLIC_API}upload/`, true);
    xhr.responseType = 'json';

    xhr.addEventListener('load', () => {
      const { response } = xhr;

      if (!response || response.error) {
        console.log(
          response && response.error && response.error.message
            ? response.error.message
            : `Couldn't upload file: ${file.name}.`,
        );
      }

      resolve(response.url);
    });

    // const headers = {}
    // for (const headerName of Object.keys(headers)) {
    //   xhr.setRequestHeader(headerName, headers[headerName])
    // }
    // xhr.withCredentials = false

    const data = new FormData();
    data.append('upload', file);

    xhr.send(data);
  });
}
