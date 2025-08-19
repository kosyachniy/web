import Head from 'next/head';
import Link from 'next/link';
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';

import styles from '../styles/auth.module.css';
import { locales } from '../components/Forms/Locale';

const continents = [{
  title: 'European',
  locales: [
    'en', 'es', 'de', 'fr', 'pt', 'it', 'pl', 'nl', 'cs', 'el', 'hu', 'sv',
    'ro', 'sk', 'fi', 'bg', 'uk', 'no', 'hr', 'sr', 'lt', 'sl', 'ca', 'lv',
    'et', 'bs', 'cy', 'eu', 'ga', 'gl', 'la', 'lb', 'mt',
  ],
}, {
  title: 'Asian',
  locales: [
    'zh', 'ja', 'ko', 'vi', 'id', 'da', 'th', 'hi', 'ms', 'jv', 'su', 'tl',
    'mn', 'ug', 'mr', 'bn', 'gu', 'or', 'ta', 'te', 'kn', 'ml', 'si', 'my',
    'km',
  ],
}, {
  title: 'CIS',
  locales: [
    'ru', 'be', 'az', 'uz', 'tt', 'ky', 'kk', 'tg', 'ka', 'hy',
  ],
}, {
  title: 'Arabic',
  locales: [
    'ar', 'fa',
  ],
}, {
  title: 'African',
  locales: [
    'af', 'so', 'ny', 'xh', 'zu', 'sw', 'mg', 'yo',
  ],
}, {
  title: 'Other',
  locales: [
    'tr', 'he', 'eo', 'is', 'ht', 'ku', 'mi', 'sq', 'mk', 'yi', 'ur', 'ps',
    'ne', 'pa', 'lo',
  ],
}];

export default ({ url }) => (
  <>
    <Head>
      <title>Choose your language</title>
      <meta name="title" content="Choose your language" />
      <link rel="canonical" href={`${process.env.NEXT_PUBLIC_WEB}locale`} />
    </Head>
    <div className={styles.auth}>
      { continents.map(continent => (
        <div className="row" key={continent.title}>
          <h2 className="mt-4">{continent.title}</h2>
          { locales.map(locale => (continent.locales.indexOf(locale.code) !== -1 && (
            <Link
              key={locale.code}
              href={url}
              locale={locale.code}
              className="col-6 col-md-4"
            >
              {`${locale.flag} ${locale.title} (${locale.name})`}
            </Link>
          ))) }
        </div>
      )) }
    </div>
  </>
);

export const getServerSideProps = async ({ query, locale }) => ({
  props: {
    ...await serverSideTranslations(locale, ['common']),
    url: query.url || '/',
  },
});
