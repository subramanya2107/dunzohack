import axios from 'axios';

const defaultparams = {
    method: 'GET',
    body: false
}

export default function request(url, params = defaultparams) {
    const { method, body } = params
    const requestBody = {
        method,
        url
    }
    const headers = {
        'content-type': 'application/json'
    }
    requestBody.headers = headers
    if (body) requestBody.data = body
    return axios({ ...requestBody })
        .then(response => response.data)
        .catch(error => error.response)
}