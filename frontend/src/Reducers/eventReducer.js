import { createSlice } from '@reduxjs/toolkit'

const eventListSlice = createSlice({name:'events', initialState:[], reducers:{
  setEvents(state, action){
    return action.payload
  },
  appendEvent(state, action){
    state.push(action.payload)
  }
}})

const eventProfileSlice = createSlice({name:'event', initialState:null, reducers:{
  setEvent(state, action){
    return action.payload
  }
}})

export const {setEvents, appendEvent} = eventListSlice.actions
export {eventProfileSlice} 
export const {setEvent} = eventProfileSlice.actions
export default eventListSlice.reducer