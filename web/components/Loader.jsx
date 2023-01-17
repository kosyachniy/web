import { useState } from 'react'
import { useSelector } from 'react-redux'

import styles from '../styles/loader.module.css'


export default () => {
    const system = useSelector(state => state.system)
    const main = useSelector(state => state.main)
    const [displayed, setDisplayed] = useState(true)

    const fadeOut = () => {
        let fadeTarget = document.getElementById("loader")

        if (!fadeTarget.style.opacity) {
            fadeTarget.style.opacity = 1
        }

        let fadeEffect = setInterval(function () {
            if (fadeTarget.style.opacity > 0) {
                fadeTarget.style.opacity -= 0.05
            } else {
                clearInterval(fadeEffect)
                fadeTarget.remove()
            }
        }, 20)
    }

    if (system.loaded && displayed) {
        setDisplayed(false)
        // fadeOut()
    }

    return (
        <div id="loader" className={ styles.loader }> {/* `bg-${main.theme}` */}
            <div>
                <img src={ `/brand/logo_${main.color}.svg` } alt="loader" />
            </div>
        </div>
    )
}
