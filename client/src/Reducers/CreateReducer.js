const getReducerFromObject = (object, initialState) => {
    const obj = object
    obj.default = obj.default || (state => state)
    return (state, { type, payload }) => (obj[type] || obj.default)(state || initialState, payload)
}

export default getReducerFromObject