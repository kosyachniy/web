import { useSelector, useDispatch } from 'react-redux'

import { popupSet } from '../store'
import styles from '../styles/popup.module.css'


export default ({ children }) => {
    const dispatch = useDispatch()
    const system = useSelector((state) => state.system)

    return (
        <div className={ styles.popup }>
            <div className={ styles.popup_back } onClick={ () => dispatch(popupSet(null)) } />
            <div className={ styles.popup_cont}> {/* bg-${ system.theme }` */}
                { children }
            </div>
        </div>
    )
}
