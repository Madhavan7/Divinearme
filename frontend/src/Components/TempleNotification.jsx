import TempleNotificationCSS from './TempleNotification.module.css'

const TempleNotification = ({data}) =>{
  return (<div className={TempleNotificationCSS.notification}>
    <div>{data.name}</div>
    <div>{data.temple_location}</div>
  </div>)

}

export default TempleNotification