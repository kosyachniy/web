export const systemLoaded = () => ({
    type: 'SYSTEM_LOADED',
})

export const popupSet = popup => ({
    type: 'SYSTEM_POPUP',
    popup,
})

export const searching = search => ({
    type: 'SEARCH',
    search,
})
