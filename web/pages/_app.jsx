import { useEffect } from 'react';
import { connect, useSelector } from 'react-redux';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { appWithTranslation } from 'next-i18next';

import '../styles/main.scss';
import '../styles/main.css';
import styles from '../styles/body.module.css';
import wrapper from '../redux/store';
import { changeLang, setToken, setUtm } from '../redux/actions/main';
import { onlineAdd, onlineDelete, onlineReset } from '../redux/actions/online';
import { categoriesGet, categoriesClear } from '../redux/actions/categories';
import api from '../lib/api';
import generate from '../lib/generate';
import socketIO from '../lib/sockets';

import Header from '../components/Structure/Header';
import Footer from '../components/Structure/Footer';
import Auth from '../components/Auth';
import AuthMail from '../components/Auth/Mail';
import Online from '../components/Online';
import Toasts from '../components/Toast';

const Body = ({
  system, main, online, categories,
  changeLang, setToken, setUtm,
  onlineAdd, onlineDelete, onlineReset,
  categoriesGet, categoriesClear,
  Component, pageProps,
}) => {
  const router = useRouter();
  const rehydrated = useSelector(state => state._persist.rehydrated); /* eslint-disable-line */

  // Bootstrap
  useEffect(() => {
    window.bootstrap = require('bootstrap/dist/js/bootstrap');
  }, []);

  // Online
  useEffect(() => {
    if (main.token && !online.count) {
      socketIO.emit('online', { token: main.token });
      socketIO.on('online_add', x => onlineAdd(x));
      socketIO.on('online_del', x => onlineDelete(x));
      socketIO.on('disconnect', () => onlineReset());
    }
  }, [router.asPath, main.token]);

  useEffect(() => {
    if (rehydrated && router.isReady) {
      // UTM
      let { utm } = main;
      if (router.query.utm && !utm) {
        utm = router.query.utm;
        setUtm(utm);
      }

      // Generate token
      if (!main.token) {
        const token = generate();
        api(main, 'account.token', {
          token,
          network: 'web',
          utm,
          extra: {
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            languages: navigator.languages,
          },
        }, true).then(() => setToken(token));
      }
    }
  }, [rehydrated, router.isReady, router.query]);

  useEffect(() => {
    categoriesClear();
  }, [main.locale]);

  useEffect(() => {
    if (main.token && categories === null) {
      api(main, 'categories.get', { locale: main.locale }).then(
        res => categoriesGet(res.categories),
      );
    }
  }, [main.token, categories]);

  useEffect(() => {
    changeLang(router.locale);
  }, [router.locale]);

  return (
    <>
      <Head>
        {/* SEO */}
        <title>{ process.env.NEXT_PUBLIC_NAME }</title>
        <meta name="title" content={process.env.NEXT_PUBLIC_NAME} />
        <meta name="og:title" content={process.env.NEXT_PUBLIC_NAME} />
        <meta name="description" content={router.locale === 'en' ? 'Template Web App' : 'Шаблонное веб-приложение'} />
        <meta name="og:description" content={router.locale === 'en' ? 'Template Web App' : 'Шаблонное веб-приложение'} />
        <meta name="og:image" content={`${process.env.NEXT_PUBLIC_WEB}brand/logo_dark.svg`} />
        <meta property="og:type" content="website" />

        {/* Zoom */}
        <meta
          name="viewport"
          content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no"
        />
      </Head>

      <Header />

      <div className={`bg-${main.theme}`}>
        <div className={`container ${styles.main}`}>
          <Component {...pageProps} />
        </div>
      </div>

      { system.popup === 'auth' && (
        <Auth />
      ) }
      { system.popup === 'mail' && (
        <AuthMail />
      ) }
      { system.popup === 'online' && (
        <Online />
      ) }

      <Toasts toasts={system.toasts} />

      <Footer />
    </>
  );
};

export default wrapper.withRedux(appWithTranslation(connect(state => state, {
  changeLang,
  setToken,
  setUtm,
  onlineAdd,
  onlineDelete,
  onlineReset,
  categoriesGet,
  categoriesClear,
})(Body)));
