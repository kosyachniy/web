import React from 'react';
import './style.css';
import Popup from '../../../components/Popup';


const Auth = (props) => {
    const { system, handlerPopUp } = props

    return (
        <div id="auth">
            <Popup handlerPopUp={handlerPopUp} theme={system.theme} >
                <div
                    id="mail"
                    className="btn"
                    onClick={ ()=>{handlerPopUp('mail')} }
                >
                    <i className="bi bi-envelope-fill" />
                </div>
                <a
                    href={`https://oauth.vk.com/authorize?client_id=${process.env.REACT_APP_VK_ID}&display=popup&redirect_uri=${process.env.REACT_APP_CLIENT}callback&scope=4194304&response_type=code&v=5.103`}
                    className="btn btn_vk"
                    onClick={() => localStorage.setItem('previousPath', document.location.href)}
                >
                    <i className="fab fa-vk" />
                </a>
                <a
                    href={`https://accounts.google.com/o/oauth2/auth?redirect_uri=${process.env.REACT_APP_CLIENT}callback&response_type=code&client_id=${process.env.REACT_APP_GOOGLE_ID}&scope=https://www.googleapis.com/auth/userinfo.email%20https://www.googleapis.com/auth/userinfo.profile`}
                    className="btn btn_g"
                    onClick={() => localStorage.setItem('previousPath', document.location.href)}
                >
                    <i className="fab fa-google" />
                </a>
                <a
                    href={`https://t.me/retestme?start=<token>`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn btn_tg"
                    onClick={() => localStorage.setItem('previousPath', document.location.href)}
                >
                    <i className="fab fa-telegram-plane" />
                </a>
            </Popup>
        </div>
    );
};

export default Auth;
