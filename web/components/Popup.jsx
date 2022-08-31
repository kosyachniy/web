import styles from '../styles/popup.module.css'


export default ({ children, handlerPopUp, theme='light' }) => {
    return (
        <div className="popup">
            <div className="popup_back" onClick={ ()=>{handlerPopUp(false)} } />
            <div className={`popup_cont bg-${ theme }`}>
                { children }
            </div>
        </div>
    )
}
