async function serverRequest(method = '', data = {}, external=true) {
  let url = external ? process.env.NEXT_PUBLIC_API : 'http://api:5000/';
  url += method.replace('.', '/') + (method ? '/' : '');
  return fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      // TODO: ssr get cookie
    },
    body: JSON.stringify(data),
  });
}

const api = (main=null, method, data={}, setted=false, external=true) => new Promise((resolve, reject) => {
  // TODO: reject errors
  serverRequest(method, data, external).then(async (response) => {
    if (!response.ok) {
      if (response.status === 401 && !setted) {
        // TODO: auto request on token creation
        await api(main, 'account.token', {
          token: main.token,
          network: 'web',
          utm: main.utm,
          extra: {
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            languages: navigator.languages,
          },
        }, true, external);
        resolve(await api(main, method, data, true, external));
      } else {
        const text = await response.text();
        console.log('Error', response.status, text);
        reject(text);
      }
    } else {
      resolve(await response.json());
    }
  });
});

export default api;
