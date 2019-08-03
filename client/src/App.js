import React from 'react';
import Dashboard from './Pages/Dashboard'
import { Provider } from 'react-redux'
import configureStore from './store'
import 'antd/dist/antd.css'
import './App.scss';

const store = configureStore()

const App = () =>
  <Provider store={store}>
    <Dashboard />
  </Provider>

export default App;
