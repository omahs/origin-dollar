import React from 'react'
import Document, { Html, Head, Main, NextScript } from 'next/document'

class MyDocument extends Document {
  render() {
    return (
      <Html>
        <Head>
          <link
            rel="shortcut icon"
            href="/images/favicon.ico"
            type="image/x-icon"
          />
          <link rel="icon" href="/images/favicon.ico" type="image/x-icon" />
          <Head>
            <link
              href="https://fonts.googleapis.com/css2?family=Courier+Prime:wght@700&family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap"
              rel="stylesheet"
            />
            {/* jQuery is required for bootstrap javascript */}
            <NextScript
              src="https://code.jquery.com/jquery-3.6.0.slim.min.js"
              integrity="sha384-Qg00WFl9r0Xr6rUqNLv1ffTSSKEFFCDCKVyHZ+sVt8KuvG99nWw5RNvbhuKgif9z"
            />
            <NextScript
              src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"
              integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo"
            />
          </Head>

          {/* Twitter ads tracking */}
          <NextScript
            src="//static.ads-twitter.com/oct.js"
            type="text/javascript"
          />

          <meta property="og:url" content="https://ousd.com" />
          <meta property="og:type" content="website" />
          <meta property="og:title" content="Origin Dollar (OUSD)" />
          <meta
            property="og:description"
            content="A fully transparent stablecoin that earns a yield from DeFi"
          />
          <meta name="twitter:card" content="summary_large_image" />
          <meta name="twitter:site" content="@originprotocol" />
          <meta name="twitter:title" content="Origin Dollar (OUSD)" />
          <meta
            name="twitter:description"
            content="A fully transparent stablecoin that earns a yield from DeFi"
          />
          {/* If not on localhost and request's protocl was HTTP, redirect to HTTPS */}
          <NextScript
            dangerouslySetInnerHTML={{
              __html: `
            var href = window.location.href;
            var isLocal = /^http:\\/\\/localhost(.*)$/.exec(href);
            var http = /^http:\\/\\/(.*)$/.exec(href);
            if (!isLocal && http) {
              window.location.replace('https://' + http[1]);
            }
          `,
            }}
          />
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    )
  }
}

export default MyDocument
