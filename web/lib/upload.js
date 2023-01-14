export default function upload(re) {
    return new Promise((resolve) => {
		const xhr = new XMLHttpRequest()
		xhr.open('POST', `${process.env.NEXT_PUBLIC_API}upload/`, true)
		xhr.responseType = 'json'

		xhr.addEventListener('load', () => {
			const response = xhr.response

			if (!response || response.error) {
				console.log(
                    response
                    && response.error
                    && response.error.message ?
                        response.error.message :
                        genericErrorText
                )
			}

			resolve(response.url)
		} )

		// const headers = {}
		// for (const headerName of Object.keys(headers)) {
		// 	xhr.setRequestHeader(headerName, headers[headerName])
		// }
		// xhr.withCredentials = false

		const data = new FormData()
		data.append( 'upload', re )

		xhr.send( data )
    })
}
