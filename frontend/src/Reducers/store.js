import {configureStore, createSlice} from '@reduxjs/toolkit'
import templeListReducer from './templeReducer'
import { templeProfileSlice } from './templeReducer'
import eventListReducer, { eventProfileSlice } from './eventReducer'
import userListReducer, { userProfileSlice } from './userReducer'

const store = configureStore({
  reducer: {
    templeList:templeListReducer,
    eventList:eventListReducer,
    userList:userListReducer,
    templeProfile: templeProfileSlice.reducer,
    eventProfile: eventProfileSlice.reducer,
    userProfile: userProfileSlice.reducer,
  }
})

export default store
