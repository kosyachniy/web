export const systemPrepared = () => ({
  type: 'SYSTEM_PREPARED',
});

export const systemLoaded = () => ({
  type: 'SYSTEM_LOADED',
});

export const systemLoadedLocale = (locale) => ({
  type: 'SYSTEM_LOADED_LOCALE',
  locale,
});

export const popupSet = (popup) => ({
  type: 'SYSTEM_POPUP',
  popup,
});

export const searching = (search) => ({
  type: 'SEARCH',
  search,
});
