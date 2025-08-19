import { serverSideTranslations } from 'next-i18next/serverSideTranslations';

import { Edit } from '../../components/Post';

export default Edit;

export const getStaticProps = async ({ locale }) => ({
  props: {
    ...await serverSideTranslations(locale, ['common']),
  },
});
