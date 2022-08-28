import { useState } from 'react'
import { useSelector } from 'react-redux'

import styles from '../styles/loader.module.css'


export default () => {
    const system = useSelector((state) => state.system)

    const [state, setState] = useState({
        displayed: true,
    })

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

    if (system.loaded && state.displayed) {
        setState({ displayed: false })
        fadeOut()
    }

    return (
        <div id="loader" className={`bg-${system.theme}`}>
            <div>
                <img src={`/brand/logo_${system.color}.svg`} alt="loader" />
            </div>
        </div>
    )
}
