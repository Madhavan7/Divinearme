import axios from "axios"


export const baseUrl = "http://127.0.0.1:8000/"


export const createAccount = async (username, password) =>{
  const response = await axios.post(`${baseUrl}users/create/`, {username, password})
  return response.data
}

export const login = async (username, password) =>{
  const response = await axios.post(`${baseUrl}api/token/`, {username, password})
  window.localStorage.setItem('tokens',JSON.stringify(response.data))
  return response.data
}

export default {createAccount}