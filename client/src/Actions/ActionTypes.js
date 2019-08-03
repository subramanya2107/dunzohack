import * as constants from '../Constants/constants'

// reducer actions
export const setStore = payload => ({ type: constants.SET_STORE, payload })
export const setItem = payload => ({ type: constants.SET_ITEM, payload })
export const setItemDetail = payload => ({ type: constants.SET_ITEM_DETAIL, payload })
export const setCategory = payload => ({ type: constants.SET_CATEGORY, payload })
export const resetState = () => ({ type: constants.SET_RESET })

// saga actions
export const getStore = payload => ({ type: constants.GET_STORE, payload })
export const getItem = payload => ({ type: constants.GET_ITEM, payload })
export const getItemDetail = payload => ({ type: constants.GET_ITEM_DETAIL, payload })
export const getCategory = payload => ({ type: constants.GET_CATEGORY, payload })