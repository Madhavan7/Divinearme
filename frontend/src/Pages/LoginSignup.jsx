import { useState } from "react"
import {createAccount,login} from "../Services/loginSignupService"
import { getUserId, getUserTemples } from "../Services/userService"
import { Navigate, useNavigate } from "react-router-dom"
import { useDispatch, useSelector } from "react-redux"

export const Signup = ({show}) => {
  if(!show){
    return null
  }

  const signup = (e) =>{
    e.preventDefault();
    const username = e.target.username.value
    const password = e.target.password.value
    const retype = e.target.repeat_password.value
    if(retype !== password){
      console.log('passwords dont match')
    }else{
      createAccount(username, password).then(console.log).catch(console.error)
    }

  }
  return (
  <div>
    <h2>Signup</h2>
    <form onSubmit={signup}>
      <div>Username <input name={'username'} ></input></div>
      <div>Password <input type='password' name={'password'} ></input></div>
      <div>Repeat Password <input type='password' name={'repeat_password'} ></input></div>
      <button type="submit">Signup</button>
    </form>
  </div>
  )
}

export const Login = ({show}) => {
  const navigate = useNavigate()
  if(!show){
    return null
  }

  const loginUser = async (e) =>{
    e.preventDefault()
    const username = e.target.username.value
    const password = e.target.password.value
    // await login(username, password)
    const id = await login(username, password).then(getUserId).then(r => r.id)
    navigate(`users/${id}`)
  }
  return (
  <div>
    <h2>Login</h2>
    <form onSubmit={loginUser}>
      <div>Username <input name={'username'} ></input></div>
      <div>Password <input type='password' name={'password'} ></input></div>
      <button type="submit">Login</button>
    </form>
  </div>)
}

const LoginSignupPage = () =>{
  const [signup, setSignup] = useState(true)

  const toggleSignup = () =>{
    const state = !signup
    setSignup(state)
  }

  return (
    <>
    <button onClick={toggleSignup}>{signup?'login':'signup'}</button>
    <Signup show={signup}/>
    <Login show={!signup}/>
    </>
  )

}

export default LoginSignupPage