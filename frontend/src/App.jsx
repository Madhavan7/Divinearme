import { useEffect, useState } from 'react'
import LoginSignupPage from './Pages/LoginSignup'
import {useNavigate, BrowserRouter as Router, Routes, Route} from 'react-router-dom'

export const Main = () => {
  return (<div>Menu</div>)
}
function App() {
  const [count, setCount] = useState(0)

  useEffect(() =>{

  },[])
  return (
    <>
      <Main/>
      <LoginSignupPage/>
      {/* <Routes>
        <Route path=""/>
      </Routes> */}
    </>
  )
}

export default App
