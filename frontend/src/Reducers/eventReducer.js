import createSlice from 'react-redux'

const eventSlice = createSlice({name:'event', initialState:[], reducers:{
  setEvents(state, action){
    return action.payload
  },
  appendEvent(state, action){
    state.push(action.payload)
  }
}})

export const {setEvents, appendEvent} = eventSlice.actions
export default eventSlice.reducer