import { createStore, applyMiddleware, compose } from 'redux'
import createSagaMiddleware from 'redux-saga'
import makeRootReducer from './Reducers/Reducer'
import rootSaga from './MainSagas/sagas'

const sagaMiddleware = createSagaMiddleware()
const middleware = [sagaMiddleware]

function getDevStore() {
    const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose
    const store = createStore(
        makeRootReducer(),
        composeEnhancers(applyMiddleware(...middleware))
    )
    sagaMiddleware.run(rootSaga)
    store.runSaga = sagaMiddleware.run
    return store
}

function getProdStore() {
    const store = createStore(
        makeRootReducer(),
        compose(applyMiddleware(...middleware))
    )
    sagaMiddleware.run(rootSaga)
    store.run = sagaMiddleware.run
    return store
}

const configureStore =
    process.env.NODE_ENV === 'production' ? getProdStore : getDevStore;

export default configureStore