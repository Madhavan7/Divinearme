import { createSlice } from '@reduxjs/toolkit'
import { getUserTemples } from '../Services/userService'

const templeListSlice = createSlice({name: 'temples',initialState:[], reducers:{
  setTemples(state, action){
    return action.payload
  },
  appendTemple(state, action){
    state.push(action.payload)
  }
}})

const templeProfileSlice = createSlice({name:'temple', initialState:null, reducers:{
  setTemple(state, action){
    console.log('working')
    console.log(action.payload)
    return action.payload
  }
}})

export const storeUserTemples = (id, pageNumber) =>{
  return dispatch =>{
    getUserTemples(id, pageNumber).then(r => r.results).then(response => {console.log(response);dispatch(setTemples(response))}).catch(console.error)
  }
}

export const {setTemples, appendTemple} = templeListSlice.actions
export const {setTemple} = templeProfileSlice.actions
export {templeProfileSlice} 
export default templeListSlice.reducer