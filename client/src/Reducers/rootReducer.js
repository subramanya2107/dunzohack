import { fromJS } from 'immutable'
import * as constants from '../Constants/constants'
import getReducerFromObject from './CreateReducer'

const initialState = fromJS({
    store: ''
})

const rootState = {
    [constants.SET_STORE]: (state, payload) => state.set('store', payload),
    [constants.SET_ITEM]: (state, payload) => state.set('item', payload),
    [constants.SET_ITEM_DETAIL]: (state, payload) => state.set('itemDetail', payload),
    [constants.SET_CATEGORY]: (state, payload) => state.set('category', payload),
    [constants.SET_RESET]: (state) => initialState
}

export default getReducerFromObject(rootState, initialState)

