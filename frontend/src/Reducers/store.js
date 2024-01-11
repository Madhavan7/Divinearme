import {configureStore} from 'redux'
import templeReducer from './templeReducer'
import eventReducer from './eventReducer'
import userReducer from './userReducer'

const store = configureStore({
  reducer: {
    temples:templeReducer,
    events:eventReducer,
    users:userReducer,
  }
})

