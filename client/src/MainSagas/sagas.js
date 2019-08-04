import { call, put, takeLatest, cancel } from 'redux-saga/effects'
import request from './request'
import { setStore, setItem, setItemDetail, setCategory } from '../Actions/ActionTypes'
import * as constants from '../Constants/constants'

const store = [
    {
        id: 1,
        name: 'store 1',
        address: 'address 1'
    },
    {
        id: 2,
        name: 'store 2',
        address: 'address 2'
    }
]

const item = [
    {
        id: 1,
        name: 'item 1',
        price: 'INR 23.5'
    },
    {
        id: 2,
        name: 'item 2',
        price: 'INR 30.75'
    }
]

const itemDetail = [
    {
        id: 1,
        name: 'item 1',
        category: 'Beverage',
        quantity: 21
    },
    {
        id: 2,
        name: 'item 2',
        category: 'Medicine',
        quantity: 34
    }
]

const category = [{
    id: 1,
    name: 'Food',
},
{
    id: 2,
    name: 'Groceries',
}]



function* getStore({ payload }) {
    try {
        let response
        if (payload.id)
            response = yield call(request, '/stores', { method: 'GET' })
        else
            response = yield call(request, `/stores/${payload.search}`, { method: 'GET' })
        yield put(setStore(response.stores))
    }
    catch (e) {
        return null
    }
}

function* getItem({ payload }) {
    try {
        let response
        if (payload.id)
            response = yield call(request, `/stores/${payload.id}/items`, { method: 'GET' })
        else if (payload.category_id)
            response = yield call(request, `category/${payload.category_id}/items`, { method: 'GET' })
        else
            response = yield call(request, `/items/${payload.search}`, { method: 'GET' })
        yield put(setItem(response.items))
    }
    catch (e) {
        return null
    }
}

function* getItemDetail({ payload }) {
    try {
        const response = yield call(request, `/item/${payload.id}/stores`, { method: 'GET' })
        yield put(setItemDetail(response.stores))
    }
    catch (e) {
        return null
    }
}

function* getCategory({ payload }) {
    try {
        const response = yield call(request, '/category', { method: 'GET' })
        yield put(setCategory(response.categories))
    }
    catch (e) {
        return null
    }
}

function* cancelTask(watcher) {
    yield cancel(watcher)
}

export default function* rootSaga() {
    const watcher = []
    watcher.push(yield takeLatest(constants.GET_STORE, getStore))
    watcher.push(yield takeLatest(constants.GET_ITEM, getItem))
    watcher.push(yield takeLatest(constants.GET_ITEM_DETAIL, getItemDetail))
    watcher.push(yield takeLatest(constants.GET_CATEGORY, getCategory))
    yield takeLatest('REMOVE_ALL_SAGAS', cancelTask, watcher)
}