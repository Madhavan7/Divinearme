import { createSlice } from '@reduxjs/toolkit'
import { getUser } from '../Services/userService'

const userListSlice = createSlice({name:'users', initialState:[], reducers:{
  setUsers(state, action){
    return action.payload
  },
  appendUser(state, action){
    state.push(action.payload)
  }
}})

const userProfileSlice = createSlice({name:'user', initialState:null, reducers:{
  setUser(state, action){
    return action.payload
  }
}})

const getUserProfile = (id) =>{
  return dispatch =>{
    getUser(id).then(r => {console.log(r);dispatch(setUser(r))}).catch(console.error)
  } 
}

export const {setUsers, appendUser} = userListSlice.actions
export const {setUser} = userProfileSlice.actions
export {userProfileSlice}
export {getUserProfile}
export default userListSlice.reducer