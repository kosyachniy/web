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
            // TODO: ssr get cookie
        },
        body: JSON.stringify(data),
    })
}

const api = (token, locale, method, data={}, setted=false) => {
    return new Promise((resolve, reject) => {
        // data.locale = locale

        serverRequest(method, data).then(async (response) => {
            if (response.status >= 200 && response.status < 300) {
                const res = await response.json();
                resolve(res === undefined ? {} : res);
                return;
            };

            if (response.status === 401 && !setted) {
                // TODO: auto request on token creation
                await api(token, locale, 'account.token', {
                    token,
                    network: 'web',
                }, setted=true);
                resolve(await api(token, locale, method, data, true));
                return;
            }

            console.log(response);
        });
    });
}

export default api;
