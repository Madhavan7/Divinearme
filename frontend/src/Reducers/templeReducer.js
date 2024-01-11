import createSlice from 'react-redux'
import { getUserTemples } from '../Services/userService'

const templeSlice = createSlice({name: 'temple',initialState:[], reducers:{
  setTemples(state, action){
    return action.payload
  },
  appendTemple(state, action){
    state.push(action.payload)
  }
}})

export const storeUserTemples = (id, pageNumber) =>{
  getUserTemples(id, pageNumber).then(response => dispatch(setTemples(response))).catch(console.error)
}

export const {setTemples, appendTemple} = templeSlice.actions
export default templeSlice.reducer