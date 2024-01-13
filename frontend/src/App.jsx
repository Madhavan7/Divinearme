import store from './Reducers/store'
import { useEffect, useState } from 'react'
import LoginSignupPage from './Pages/LoginSignup'
import {useNavigate, BrowserRouter as Router, Routes, Route} from 'react-router-dom'
import { Provider } from 'react-redux'
import UserProfile from './Pages/UserProfile'

import AppCSS from './App.module.css'

export const Main = () => {
  return (<div className={AppCSS.main}>
    <div >Menu</div>
    <div>Logout</div>
    </div>)
}
function App() {
  
  return (
    <div>
      <Main/>
      <Routes>
        <Route path='/' element= {<Provider store={store}><LoginSignupPage/></Provider>}/>
        <Route path="users/:id" element={<Provider store={store}><UserProfile /></Provider>}/>
      </Routes>
    </div>
  )
}

export default App
