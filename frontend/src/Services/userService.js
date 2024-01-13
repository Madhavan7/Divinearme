import axios from "axios"
import {baseUrl } from "./loginSignupService"

export const getAuthToken = () =>{
  const authorizationToken = `Bearer ${JSON.parse(window.localStorage.getItem('tokens')).access}`
  return authorizationToken
}
export const getUserId = async () =>{
  const authorizationToken = getAuthToken()
  const response = await axios.get(`${baseUrl}id/`, { headers: { Authorization: authorizationToken } })
  return response.data
}

export const getUser = async (id) =>{
  const authorizationToken = getAuthToken()
  const response = await axios.get(`${baseUrl}/users/${id}/`, { headers: { Authorization: authorizationToken } })
  console.log(response.data)
  return response.data
}

export const getUserTemples = async (id, pageNumber) =>{
  const authorizationToken = getAuthToken()
  try {
    const response = await axios.get(`${baseUrl}users/${id}/temples/`, { headers: { Authorization: authorizationToken } }, { params: { 'page': pageNumber } })
    return response.data
  } catch (data) {
    return console.error(data)
  }
}

export const getUserEvents = (id, pageNumber) =>{
  const authorizationToken = getAuthToken()
  axios.get(`${baseUrl}users/${id}/events/`, {headers:{Authorization:authorizationToken}}, {params: {'page': pageNumber}}).then(response =>response.data).catch(console.error)
}

