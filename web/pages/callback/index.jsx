import { useEffect } from 'react';
import { connect } from 'react-redux';
import { useRouter } from 'next/router';
import { useTranslation } from 'next-i18next';
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';

import { popupSet, toastAdd } from '../../redux/actions/system';
import { profileIn } from '../../redux/actions/profile';
import api from '../../lib/api';

const Container = ({
  main,
  toastAdd, profileIn, popupSet,
}) => {
  const { t } = useTranslation('common');
  const router = useRouter();

  const onSocial = (type, code) => api(main, 'users.social', {
    social: type,
    code,
    utm: main.utm,
  }).then(res => {
    profileIn(res);
    popupSet(null);
    router.push(localStorage.getItem('previousPath') || '/profile');
  }).catch(err => toastAdd({
    header: t('system.error'),
    text: err,
    color: 'white',
    background: 'danger',
  }));

  useEffect(() => {
    if (main.token) {
      const params = Object.fromEntries(new URLSearchParams(document.location.search));
      if (params.code) {
        const { code } = params;
        if (code === undefined) {
          router.push('/');
        }

        let type;
        if (document.location.search.indexOf('google') !== -1) {
          type = 'g';
        } else if (document.location.search.indexOf('telegram') !== -1) {
          type = 'tg';
        } else if (document.location.search.indexOf('state=fb') !== -1) {
          type = 'fb';
        } else {
          type = 'vk';
        }

        onSocial(type, code);
      } else {
        router.push('/');
      }
    }
  }, [main.token]);

  return (
    <></>
  );
};

export default connect(state => state, { toastAdd, profileIn, popupSet })(Container);

export const getStaticProps = async ({ locale }) => ({
  props: {
    ...await serverSideTranslations(locale, ['common']),
  },
});
