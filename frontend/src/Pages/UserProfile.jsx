import { useEffect, useState } from "react"
import { useDispatch, useSelector, useStore } from "react-redux"
import { useMatch, useNavigate } from "react-router-dom"
import { getUserId } from "../Services/userService"
import { storeUserTemples } from "../Reducers/templeReducer"
import TempleNotification from "../Components/TempleNotification"
import { getUserProfile } from "../Reducers/userReducer"
import UserProfileCSS from './UserProfile.module.css'

const UserProfile = () =>{
  const navigate = useNavigate()
  const match = useMatch('users/:id')
  const dispatch = useDispatch()
  const temples = useSelector(state =>state.templeList)
  const profile = useSelector(state => state.userProfile)
  //below is viewing permissions
  const [isUser, setIsUser] = useState(false)
  const [canView, setCanView] = useState(false)

  //below is the page numbers for the temple and events
  const [templePageNumber, setTemplePageNumber] = useState(1)
  const [eventPageNumber, setEventPageNumber] = useState(1)

  const setVision = (id) =>{
    if(id === match.params.id){
      setIsUser(true)
      setCanView(true)
    }
  }

  useEffect(()=>{
    const temp = async () =>{
      try{
        const response = await getUserId()
        setVision(response.id)
      }catch{
        navigate('/')
      }
    }
    temp()
  }, [])

  useEffect(()=>{
    dispatch(storeUserTemples(match.params.id, 0))
  },[])

  useEffect(() =>{
    dispatch(getUserProfile(match.params.id))
  }, [])


  return(<div style={{display:"flex", flexGrow:1, height:'800px'}}>
    <div className={UserProfileCSS.profile}>
      {profile === null?'loading':profile.username}
    </div>
    <div className={UserProfileCSS.body} >
      {temples.map(temple => <TempleNotification data={temple} key={temple.id}/>)}
    </div>
  </div>)
}

export default UserProfile