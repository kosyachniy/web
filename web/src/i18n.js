import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import Backend from 'i18next-xhr-backend'


import { locale as default_locale } from './sets'


const locales = ['en', 'ru', 'es'];
let locale = localStorage.getItem('locale');
if (locale === null || locales.indexOf(locale) === -1) {
    const language = window.navigator ? (
        window.navigator.language
        || window.navigator.systemLanguage
        || window.navigator.userLanguage
    ) : default_locale;
    locale = language.substr(0, 2).toLowerCase();
    localStorage.setItem('locale', locale);
}

i18n
    .use(Backend)
    .use(initReactI18next)
    .init({
        lng: locale || default_locale,
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
