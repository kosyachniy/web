import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import Backend from 'i18next-xhr-backend'


const locales = ['en', 'ru', 'es'];
let locale = localStorage.getItem('locale');
if (locale === null || locales.indexOf(locale) === -1) {
    const language = window.navigator ? (
        window.navigator.language
        || window.navigator.systemLanguage
        || window.navigator.userLanguage
    ) : process.env.REACT_APP_LOCALE;
    locale = language.substr(0, 2).toLowerCase();
    localStorage.setItem('locale', locale);
}

i18n
    .use(Backend)
    .use(initReactI18next)
    .init({
        lng: locale || process.env.REACT_APP_LOCALE,
        fallbackLng: 'en',
        debug: false,

        interpolation: {
            escapeValue: false,
        },

        react: {
            useSuspense: false,
        },
    });

export default i18n;
