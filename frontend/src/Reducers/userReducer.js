import createSlice from 'react-redux'

const userSlice = createSlice({name:'user', initialState:[], reducers:{
  setUsers(state, action){
    return action.payload
  },
  appendUser(state, action){
    state.push(action.payload)
  }
}})

export const {setUsers, appendUser} = userSlice.actions
export default userSlice.reducer