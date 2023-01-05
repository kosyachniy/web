async function serverRequest(method='', data={}) {
    const url = (
        process.env.NEXT_PUBLIC_API
        + method.replace('.', '/')
        + (method ? '/' : '')
    )
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .catch((error) => {
        let errCode;
        const errText = error.toString();

        if (errText === 'Error: Request failed with status code 429') {
            errCode = 429;
        } else if (errText === 'Error: Network Error') {
            errCode = 'network';
        } else {
            errCode = 400;
        }

        return {
            error: errCode,
            data: errText,
        };
    });
}

export default (token, locale, method, data={}) => {
    return new Promise((resolve, reject) => {
        data.network = 'web'
        data.locale = locale
        data.token = token

        serverRequest(method, data).then(async (responce) => {
            const res = await responce.json();

            if (res.error !== 0) {
                console.log(res.data);
                reject(res.error, res.data);
            } else if (res.data === undefined) {
                resolve({});
            } else {
                resolve(res.data);
            }
        });
    });
}

// TODO: Socket.IO
