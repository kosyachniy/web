import { useState, useEffect } from 'react';
import { connect } from 'react-redux';
import { useRouter } from 'next/router';
import { useTranslation } from 'next-i18next';
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';

import styles from '../../styles/profile.module.css';
import { toastAdd } from '../../redux/actions/system';
import { profileUpdate } from '../../redux/actions/profile';
import api from '../../lib/api';
import Upload from '../../components/Forms/Upload';

// const checkPassword = password => (
//     (password.search(/\d/) !== -1) && (password.search(/[A-Za-z]/) !== -1)
// )

const Container = ({
  main, profile,
  toastAdd, profileUpdate,
}) => {
  const { t } = useTranslation('common');
  const router = useRouter();
  const [login, setLogin] = useState(profile.login || '');
  const [password, setPassword] = useState('');
  const [image, setImage] = useState(profile.image);
  const [name, setName] = useState(profile.name || '');
  const [surname, setSurname] = useState(profile.surname || '');
  const [phone, setPhone] = useState(profile.phone || '');
  const [mail, setMail] = useState(profile.mail || '');
  // const [social, setSocial] = useState(profile.social)
  // const [status, setStatus] = useState(profile.status)

  useEffect(() => {
    if (main.token) {
      if (!profile.id) {
        router.push('/');
      }

      api(main, 'users.get', { id: +profile.id }).then(
        res => {
          profileUpdate(res.users);
          setLogin(res.users.login);
          setImage(res.users.image);
          setName(res.users.name);
          setSurname(res.users.surname);
          setPhone(res.users.phone);
          setMail(res.users.mail);
        },
      ).catch(err => toastAdd({
        header: t('system.error'),
        text: err,
        color: 'white',
        background: 'danger',
      }));
    }
  }, [main.token]);

  const accountEdit = () => {
    const data = {};
    if (login && login !== profile.login) {
      data.login = login;
    }
    if (name && name !== profile.name) {
      data.name = name;
    }
    if (surname && surname !== profile.surname) {
      data.surname = surname;
    }
    if (phone && phone !== profile.phone) {
      data.phone = phone;
    }
    if (mail && mail !== profile.mail) {
      data.mail = mail;
    }
    if (password.length) {
      data.password = password;
    }
    if (image !== profile.image) {
      data.image = image;
    }

    api(main, 'account.save', data).then(() => {
      profileUpdate({
        login, image, name, surname, phone, mail,
      });
      toastAdd({
        header: t('system.success'),
        text: t('system.saved'),
        color: 'white',
        background: 'success',
      });
    }).catch(err => toastAdd({
      header: t('system.error'),
      text: err,
      color: 'white',
      background: 'danger',
    }));
  };

  return (
    <div className="container">
      <div className="row py-3">
        <div className="col-12 col-md-6 mb-3">
          <Upload
            image={image === '/user.png' ? null : image}
            setImage={setImage}
          />
        </div>
        <div className="col-12 col-md-6">
          <div className="input-group mb-3">
            <input
              value={name}
              onChange={event => setName(event.target.value)}
              placeholder={t('profile.name')}
              type="text"
              aria-label="First name"
              className="form-control"
            />
            <input
              value={surname}
              onChange={event => setSurname(event.target.value)}
              placeholder={t('profile.surname')}
              type="text"
              aria-label="Last name"
              className="form-control"
            />
          </div>
          <div className="input-group flex-nowrap mb-3">
            <span className="input-group-text" id="addon-wrapping">+</span>
            <input
              value={phone}
              onChange={event => setPhone(event.target.value)}
              placeholder={t('profile.phone')}
              type="text"
              className="form-control"
              aria-label="Phone number"
              aria-describedby="addon-wrapping"
            />
          </div>
          <div className="input-group flex-nowrap mb-3">
            <span className="input-group-text" id="addon-wrapping">@</span>
            <input
              value={login}
              onChange={event => setLogin(event.target.value)}
              placeholder={t('profile.login')}
              type="text"
              className="form-control"
              aria-label="Username"
              aria-describedby="addon-wrapping"
            />
          </div>
          <div className="input-group mb-3">
            <input
              value={mail}
              onChange={event => setMail(event.target.value)}
              placeholder={t('profile.mail')}
              type="email"
              className="form-control"
              autoComplete="false"
            />
          </div>
          <div className="input-group mb-3">
            <input
              value={password}
              onChange={event => setPassword(event.target.value)}
              placeholder={t('profile.password')}
              type="password"
              className="form-control"
              autoComplete="false"
            />
          </div>
        </div>
      </div>
      <button
        type="button"
        className={`${styles.btn} btn btn-success`}
        onClick={accountEdit}
      >
        <i className="fa-regular fa-floppy-disk" />
      </button>
    </div>
  );
};

export default connect(state => state, { toastAdd, profileUpdate })(Container);

export const getStaticProps = async ({ locale }) => ({
  props: {
    ...await serverSideTranslations(locale, ['common']),
  },
});
