export const popupSet = (popup) => ({
  type: 'SYSTEM_POPUP',
  popup,
});

export const toastAdd = (toast) => ({
  type: 'SYSTEM_TOAST',
  toast,
});

export const searching = (search) => ({
  type: 'SEARCH',
  search,
});
