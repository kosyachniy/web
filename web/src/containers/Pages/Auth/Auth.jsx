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
            </Popup>
        </div>
    );
};

export default Auth;
