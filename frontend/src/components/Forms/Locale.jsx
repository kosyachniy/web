import { useTranslation } from 'next-i18next';

export const locales = [{
  code: 'en', name: 'English', title: 'English', flag: '🇬🇧',
}, {
  code: 'ru', name: 'Russian', title: 'Русский', flag: '🇷🇺',
}, {
  code: 'zh', name: 'Chinese', title: '中文', flag: '🇨🇳',
}, {
  code: 'es', name: 'Spanish', title: 'Español', flag: '🇪🇸',
}, {
  code: 'de', name: 'German', title: 'Deutsch', flag: '🇩🇪',
}, {
  code: 'fr', name: 'French', title: 'Français', flag: '🇫🇷',
}, {
  code: 'ja', name: 'Japanese', title: '日本語', flag: '🇯🇵',
}, {
  code: 'pt', name: 'Portuguese', title: 'Português', flag: '🇵🇹',
}, {
  code: 'it', name: 'Italian', title: 'Italiano', flag: '🇮🇹',
}, {
  code: 'pl', name: 'Polish', title: 'Polski', flag: '🇵🇱',
}, {
  code: 'tr', name: 'Turkish', title: 'Türkçe', flag: '🇹🇷',
}, {
  code: 'nl', name: 'Dutch', title: 'Nederlands', flag: '🇳🇱',
}, {
  code: 'cs', name: 'Czech', title: 'Čeština', flag: '🇨🇿',
}, {
  code: 'ko', name: 'Korean', title: '한국어', flag: '🇰🇷',
}, {
  code: 'vi', name: 'Vietnamese', title: 'Việt ngữ', flag: '🇻🇳',
}, {
  code: 'fa', name: 'Persian', title: 'فارسی  ', flag: '🇮🇷',
}, {
  code: 'ar', name: 'Arabic', title: 'العربية', flag: '🇦🇪',
}, {
  code: 'el', name: 'Greek', title: 'Ελληνικά', flag: '🇬🇷',
}, {
  code: 'hu', name: 'Hungarian', title: 'Magyar', flag: '🇭🇺',
}, {
  code: 'sv', name: 'Swedish', title: 'Svenska', flag: '🇸🇪',
}, {
  code: 'ro', name: 'Romanian', title: 'Română', flag: '🇷🇴',
}, {
  code: 'sk', name: 'Slovak', title: 'Slovenčina', flag: '🇸🇰',
}, {
  code: 'id', name: 'Indonesian', title: 'Bahasa Indonesia', flag: '🇮🇩',
}, {
  code: 'da', name: 'Danish', title: 'Dansk', flag: '🇩🇰',
}, {
  code: 'th', name: 'Thai', title: 'ไทย', flag: '🇹🇭',
}, {
  code: 'fi', name: 'Finnish', title: 'Suomi', flag: '🇫🇮',
}, {
  code: 'bg', name: 'Bulgarian', title: 'Български език', flag: '🇧🇬',
}, {
  code: 'uk', name: 'Ukrainian', title: 'Українська', flag: '🇺🇦',
}, {
  code: 'he', name: 'Hebrew', title: 'עברית', flag: '🇮🇱',
}, {
  code: 'no', name: 'Norwegian', title: 'Norsk', flag: '🇳🇴',
}, {
  code: 'hr', name: 'Croatian', title: 'Hrvatski jezik', flag: '🇭🇷',
}, {
  code: 'sr', name: 'Serbian', title: 'Српски језик', flag: '🇷🇸',
}, {
  code: 'lt', name: 'Lithuanian', title: 'Lietuvių kalba', flag: '🇱🇹',
}, {
  code: 'sl', name: 'Slovenian', title: 'Slovenščina', flag: '🇸🇮',
}, {
  code: 'ca', name: 'Catalan', title: 'Català', flag: '🇦🇩',
}, {
  code: 'lv', name: 'Latvian', title: 'Latviešu valoda', flag: '🇱🇻',
}, {
  code: 'hi', name: 'Hindi', title: 'हिन्दी', flag: '🇮🇳',
}, {
  code: 'et', name: 'Estonian', title: 'Eesti keel', flag: '🇪🇪',
}, {
  code: 'az', name: 'Azerbaijani', title: 'Azərbaycan dili', flag: '🇦🇿',
}, {
  code: 'so', name: 'Somali', title: 'Af Soomaali', flag: '🇸🇴',
}, {
  code: 'af', name: 'Afrikaans', title: 'Afrikaans', flag: '🇿🇦',
}, {
  code: 'ms', name: 'Malay', title: 'Bahasa Melayu', flag: '🇲🇾',
}, {
  code: 'jv', name: 'Javanese', title: 'Basa Jawa', flag: '🇮🇩',
}, {
  code: 'su', name: 'Sundanese', title: 'Basa Sunda', flag: '🇮🇩',
}, {
  code: 'bs', name: 'Bosnian', title: 'Bosanski jezik', flag: '🇧🇦',
}, {
  code: 'ny', name: 'Chichewa', title: 'Chichewa', flag: '🇲🇼',
}, {
  code: 'cy', name: 'Welsh', title: 'Cymraeg', flag: '🏴󠁧󠁢󠁷󠁬󠁳󠁿',
}, {
  code: 'eo', name: 'Esperanto', title: 'Esperanto', flag: '🏳️',
}, {
  code: 'eu', name: 'Basque', title: 'Euskara', flag: '🇪🇸',
}, {
  code: 'ga', name: 'Irish', title: 'Gaeilge', flag: '🇮🇪',
}, {
  code: 'gl', name: 'Galician', title: 'Galego', flag: '🇪🇸',
}, {
  code: 'xh', name: 'Xhosa', title: 'isiXhosa', flag: '🇿🇦',
}, {
  code: 'zu', name: 'Zulu', title: 'isiZulu', flag: '🇿🇦',
}, {
  code: 'is', name: 'Icelandic', title: 'Íslenska', flag: '🇮🇸',
}, {
  code: 'sw', name: 'Swahili', title: 'Kiswahili', flag: '🇹🇿',
}, {
  code: 'ht', name: 'Haitian Creole', title: 'Kreyòl Ayisyen', flag: '🇭🇹',
}, {
  code: 'ku', name: 'Kurdish', title: 'Kurdî', flag: '🇮🇶',
}, {
  code: 'la', name: 'Latin', title: 'Latīna', flag: '🏳️',
}, {
  code: 'lb', name: 'Luxembourgish', title: 'Lëtzebuergesch', flag: '🇱🇺',
}, {
  code: 'mg', name: 'Malagasy', title: 'Malagasy', flag: '🇲🇬',
}, {
  code: 'mt', name: 'Maltese', title: 'Malti', flag: '🇲🇹',
}, {
  code: 'mi', name: 'Maori', title: 'Māori', flag: '🇳🇿',
}, {
  code: 'uz', name: 'Uzbek', title: "O'zbek tili", flag: '🇺🇿',
}, {
  code: 'sq', name: 'Albanian', title: 'Shqip', flag: '🇦🇱',
}, {
  code: 'tl', name: 'Tagalog', title: 'Tagalog', flag: '🇵🇭',
}, {
  code: 'tt', name: 'Tatar', title: 'Tatarça', flag: '🇷🇺',
}, {
  code: 'yo', name: 'Yoruba', title: 'Yorùbá', flag: '🇳🇬',
}, {
  code: 'be', name: 'Belarusian', title: 'Беларуская мова', flag: '🇧🇾',
}, {
  code: 'ky', name: 'Kyrgyz', title: 'Кыр', flag: '🇰🇬',
}, {
  code: 'kk', name: 'Kazakh', title: 'Қазақ тілі', flag: '🇰🇿',
}, {
  code: 'mk', name: 'Macedonian', title: 'Македонски јазик', flag: '🇲🇰',
}, {
  code: 'mn', name: 'Mongolian', title: 'Монгол хэл', flag: '🇲🇳',
}, {
  code: 'tg', name: 'Tajik', title: 'Тоҷикӣ', flag: '🇹🇯',
}, {
  code: 'ka', name: 'Georgian', title: 'ქართული', flag: '🇬🇪',
}, {
  code: 'hy', name: 'Armenian', title: 'Հայերեն', flag: '🇦🇲',
}, {
  code: 'yi', name: 'Yiddish', title: 'ייִדיש', flag: '🇮🇱',
}, {
  code: 'ug', name: 'Uyghur', title: 'ئۇيغۇرچە', flag: '🇨🇳',
}, {
  code: 'ur', name: 'Urdu', title: 'اردو', flag: '🇵🇰',
}, {
  code: 'ps', name: 'Pashto', title: 'پښتو', flag: '🇦🇫',
}, {
  code: 'ne', name: 'Nepali', title: 'नेपाली', flag: '🇳🇵',
}, {
  code: 'mr', name: 'Marathi', title: 'मराठी', flag: '🇮🇳',
}, {
  code: 'bn', name: 'Bengali', title: 'বাংলা', flag: '🇧🇩',
}, {
  code: 'pa', name: 'Punjabi', title: 'ਪੰਜਾਬੀ', flag: '🇵🇰',
}, {
  code: 'gu', name: 'Gujarati', title: 'ગુજરાતી', flag: '🇮🇳',
}, {
  code: 'or', name: 'Oriya', title: 'ଓଡ଼ିଆ', flag: '🇮🇳',
}, {
  code: 'ta', name: 'Tamil', title: 'தமிழ்', flag: '🇮🇳',
}, {
  code: 'te', name: 'Telugu', title: 'తెలుగు', flag: '🇮🇳',
}, {
  code: 'kn', name: 'Kannada', title: 'ಕನ್ನಡ', flag: '🇮🇳',
}, {
  code: 'ml', name: 'Malayalam', title: 'മലയാളം', flag: '🇮🇳',
}, {
  code: 'si', name: 'Sinhala', title: 'සිංහල', flag: '🇱🇰',
}, {
  code: 'lo', name: 'Lao', title: 'ພາສາລາວ', flag: '🇱🇦',
}, {
  code: 'my', name: 'Burmese', title: 'ဗမာစာ', flag: '🇲🇲',
}, {
  code: 'km', name: 'Khmer', title: 'ភាសាខ្មែរ', flag: '🇰🇭',
}];

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
        <option value="" defaultValue>{ `🌎 ${t('system.worldwide')}` }</option>
        { locales.map(loc => (
          <option value={loc.code}>
            {loc.flag}
            {' '}
            {loc.title}
            {' '}
            (
            {loc.name}
            )
          </option>
        )) }

      </select>
    </div>
  );
};
