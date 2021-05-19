import React, {useState} from 'react';

import './style.css';


const Loader = (props) => {
    const { loaded, theme, color } = props;

    const [state, setState] = useState({
        displayed: true,
    })

    const fadeOut = () => {
        let fadeTarget = document.getElementById("loader");

        if (!fadeTarget.style.opacity) {
            fadeTarget.style.opacity = 1;
        }

        let fadeEffect = setInterval(function () {
            if (fadeTarget.style.opacity > 0) {
                fadeTarget.style.opacity -= 0.05;
            } else {
                clearInterval(fadeEffect);
                fadeTarget.remove();
            }
        }, 20);
    }

    if (loaded && state.displayed) {
        setState({ displayed: false })
        fadeOut();
    }

    return (
        <div id="loader" className={`bg-${theme}`}>
            <div>
                <img src={`/brand/logo_${color}.svg`} alt="loader" />
            </div>
        </div>
    );
};

export default Loader;
