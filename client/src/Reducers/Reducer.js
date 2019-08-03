import { combineReducers } from 'redux'
import root from './rootReducer'

const makeRootReducer = () => {
    return combineReducers({
        root
    })
}

export default makeRootReducer