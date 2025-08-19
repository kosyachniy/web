import Document, {
  Html, Head, Main, NextScript,
} from 'next/document';

export default class MyDocument extends Document {
  render() {
    return (
      <Html>
        <Head>
          <link rel="icon" type="image/png" href="/favicon.ico" />

          {/* Icons */}
          <link
            rel="stylesheet"
            href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.3/font/bootstrap-icons.css"
            crossOrigin="anonymous"
            referrerPolicy="origin-when-cross-origin"
          />
          <link
            rel="stylesheet"
            href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css"
            integrity="sha512-MV7K8+y+gLIBoVD59lQIYicR65iaqukzvf/nwasF0nqhPay5w/9lJmVM2hMDcnK1OnMGCdVK+iQrJ7lzPJQd1w=="
            crossOrigin="anonymous"
            referrerPolicy="origin-when-cross-origin"
          />
        </Head>
        <body>
          <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{
              __html: JSON.stringify({
                '@context': 'http://schema.org/',
                '@type': 'Organization',
                url: process.env.NEXT_PUBLIC_WEB,
                name: process.env.NEXT_PUBLIC_NAME,
                logo: `${process.env.NEXT_PUBLIC_WEB}brand/logo.png`,
                // "sameAs": [],
              }),
            }}
          />
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}
