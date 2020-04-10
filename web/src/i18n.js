import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import Backend from 'i18next-xhr-backend';


const langs = ['en', 'ru'];


const lang = localStorage.getItem('lang');
if (lang === null || langs.indexOf(lang) === -1) {
	const language = window.navigator ? (window.navigator.language
	|| window.navigator.systemLanguage
	|| window.navigator.userLanguage) : 'en';
	const langTemp = language.substr(0, 2).toLowerCase();
	localStorage.setItem('lang', langTemp);
}

i18n
	.use(Backend)
	.use(initReactI18next)
	.init({
		lng: localStorage.getItem('lang') || 'en',
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
