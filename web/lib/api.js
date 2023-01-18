async function serverRequest(method = '', data = {}) {
  const url = (
    process.env.NEXT_PUBLIC_API
        + method.replace('.', '/')
        + (method ? '/' : '')
  );
  return fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      // TODO: ssr get cookie
    },
    body: JSON.stringify(data),
  });
}

const api = (main, method, data = {}, setted = false) => new Promise((resolve) => {
  // TODO: reject errors
  serverRequest(method, data).then(async (response) => {
    if (!response.ok) {
      if (response.status === 401 && !setted) {
        // TODO: auto request on token creation
        await api(main, 'account.token', {
          token: main.token,
          network: 'web',
          utm: main.utm,
        }, true);
        resolve(await api(main, method, data, true));
      } else {
        const text = await response.text();
        console.log('Error', response.status, text);
        resolve(text);
      }
    } else {
      resolve(await response.json());
    }
  });
});

export default api;
