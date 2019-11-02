import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import Backend from 'i18next-xhr-backend';


if (localStorage.getItem('lang') === null) {
	const language = window.navigator ? (window.navigator.language
	|| window.navigator.systemLanguage
	|| window.navigator.userLanguage) : 'en';
	const langTemp = language.substr(0, 2).toLowerCase();
	const languageTemp = { main: langTemp, ladders: langTemp };
	localStorage.setItem('lang', JSON.stringify(languageTemp));
}

i18n
	.use(Backend)
	.use(initReactI18next)
	.init({
		lng: JSON.parse(localStorage.getItem('lang')).main || 'en',
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
