import { useTranslation } from 'next-i18next';

export default ({ locale, setLocale }) => {
  const { t } = useTranslation('common');

  return (
    <div className="input-group mb-3">
      <label className="input-group-text" htmlFor="categoryLocale">
        { t('system.locale') }
      </label>
      <select
        className="form-select"
        id="categoryLocale"
        value={locale || ''}
        onChange={event => setLocale(event.target.value)}
      >
        <option value="" defaultValue>
          🌎
          { t('system.worldwide') }
        </option>
        <option value="en">🇬🇧 English</option>
        <option value="ru">🇷🇺 Русский</option>
      </select>
    </div>
  );
};
