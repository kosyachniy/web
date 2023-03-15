import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useRouter } from 'next/router';
import Link from 'next/link';
import Image from 'next/image';
import { useTranslation } from 'next-i18next';

import styles from '../../styles/header.module.css';
import { popupSet, toastAdd, searching } from '../../redux/actions/system';
import { changeTheme } from '../../redux/actions/main';
import { profileOut } from '../../redux/actions/profile';
import api from '../../lib/api';
import Hexagon from '../Hexagon';

const Logo = () => {
  const main = useSelector(state => state.main);

  return (
    <Link href="/" className="navbar-brand">
      <img
        src={`/brand/logo_${main.color}.svg`}
        alt={process.env.NEXT_PUBLIC_NAME}
      />
    </Link>
  );
};

const Navigation = () => {
  const { t } = useTranslation('common');
  const main = useSelector(state => state.main);
  const categories = useSelector(state => state.categories);

  return (
    <>
      <li className="nav-item dropdown">
        <Link href="/posts/" className="nav-link">
          { t('structure.posts') }
        </Link>
        <ul className={`${styles.menu} dropdown-menu dropdown-menu-${main.theme}`}>
          { categories && categories.map(category => (category.id && category.status ? (
            <Link
              href={`/posts/${category.url}/`}
              className="dropdown-item"
              key={category.id}
            >
              { category.title }
            </Link>
          ) : (
            <React.Fragment key={category.id} />
          ))) }
        </ul>
      </li>
      {/* { categories && categories.map(category => (category.id && category.status ? (
        <li className="nav-item dropdown">
          <Link href={`/posts/${category.url}/`} className="nav-link">
            { category.title }
          </Link>
          { category.categories && category.categories.length ? (
            <ul className={`${styles.menu} dropdown-menu dropdown-menu-${main.theme}`}>
              { category.categories.map(subcategory => (
                <Link
                  href={`/posts/${subcategory.url}/`}
                  className="dropdown-item"
                  key={subcategory.id}
                >
                  { subcategory.title }
                </Link>
              )) }
            </ul>
          ) : (<></>) }
        </li>
      ) : (
        <React.Fragment key={category.id} />
      ))) } */}
      {/* <li className="nav-item">
        <Link href="/" className="nav-link">
          { t('structure.space') }
        </Link>
      </li> */}
      {/* <li className="nav-item">
        <Link href="/room/" className="nav-link">
          { t('structure.room') }
        </Link>
      </li> */}
    </>
  );
};

const Search = () => {
  const { t } = useTranslation('common');
  const dispatch = useDispatch();
  const router = useRouter();
  const system = useSelector(state => state.system);

  const search = value => {
    dispatch(searching(value));
    if (router.asPath !== '/posts') {
      router.push('/posts/');
    }
  };

  return (
    <input
      className={`${styles.search} form-control`}
      type="search"
      placeholder={t('system.search')}
      value={system.search}
      onChange={event => search(event.target.value)}
    />
  );
};

const Profile = () => {
  const { t } = useTranslation('common');
  const dispatch = useDispatch();
  const main = useSelector(state => state.main);
  const profile = useSelector(state => state.profile);

  const signOut = () => api(main, 'account.exit', {}).then(
    res => dispatch(profileOut(res)),
  ).catch(err => dispatch(toastAdd({
    header: t('system.error'),
    text: err,
    color: 'white',
    background: 'danger',
  })));

  if (!profile.id) {
    return (
      <button
        type="button"
        className="btn btn-success"
        onClick={() => dispatch(popupSet('auth'))}
      >
        { t('system.sign_in') }
      </button>
    );
  }

  return (
    <>
      <div
        className="nav-link"
        id="navbarDropdown"
        data-bs-toggle="dropdown"
        aria-haspopup="true"
        aria-expanded="false"
        style={{ padding: 0 }}
      >
        <Hexagon url={profile.image_optimize} />
      </div>
      <ul
        id="profile"
        className={`${styles.menu} dropdown-menu dropdown-menu-end dropdown-menu-${main.theme}`}
        aria-labelledby="navbarDropdown"
      >
        <Link href="/profile/" className="dropdown-item">
          <i className="bi bi-person-bounding-box me-2" />
          { t('system.profile') }
        </Link>
        {/* <Link href="/settings/" className="dropdown-item me-2">
          <i className="fa-solid fa-gear" />
          { t('system.settings') }
        </Link> */}
        {/* <Link href="/billing/" className="dropdown-item me-2">
          { t('system.billing') }
        </Link> */}
        { profile.status >= 6 && (
          <>
            <Link href={`https://docs.google.com/spreadsheets/d/${process.env.NEXT_PUBLIC_ANALYTICS_SHEET}/`} className="dropdown-item">
              <i className="bi bi-funnel-fill me-2" />
              { t('system.analytics') }
            </Link>
            <Link href="/eye/" className="dropdown-item">
              <i className="bi bi-cone-striped me-2" />
              { t('system.admin') }
            </Link>
          </>
        ) }
        <div className="dropdown-item" onClick={signOut}>
          <i className="bi bi-door-open-fill me-2" />
          { t('system.sign_out') }
        </div>
      </ul>
    </>
  );
};

export default () => {
  const router = useRouter();
  const dispatch = useDispatch();
  const main = useSelector(state => state.main);

  return (
    <nav className={`navbar sticky-top navbar-expand-lg navbar-${main.theme} bg-${main.theme}`}>
      <div className="container">
        <Logo />
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#burger"
          aria-controls="burger"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon" />
        </button>
        <div className="collapse navbar-collapse" id="burger">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            <Navigation />
          </ul>
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            <li className="nav-item">
              <Search />
            </li>
          </ul>
          <ul className="nav navbar-nav navbar-right">
            <li className={`me-4 ${styles.custom}`}>
              <i
                className={`me-3 ms-1 ${main.theme === 'dark' ? 'bi bi-sun-fill' : 'fa-solid fa-moon'}`}
                onClick={() => dispatch(changeTheme(main.theme === 'dark' ? 'light' : 'dark'))}
              />
              <Link href={router.query.url || `/locale?url=${router.asPath}`}>
                <Image
                  src={`/lang/${main.locale === 'ru' ? 'ru' : 'en'}.svg`}
                  alt={main.locale === 'ru' ? 'ru' : 'en'}
                  width={24}
                  height={24}
                />
              </Link>
              {/* <Link
                href={router.asPath}
                locale={main.locale === 'ru' ? 'en' : 'ru'}
              >
                <Image
                  src={`/lang/${main.locale}.svg`}
                  alt={main.locale}
                  width={24}
                  height={24}
                />
              </Link> */}
            </li>
            <li className="nav-item dropdown">
              <Profile />
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};
