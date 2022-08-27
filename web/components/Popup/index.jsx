import React from 'react';

import './style.css';


const Popup = (props) => {
    const { children, handlerPopUp, theme='light' } = props;

    return (
        <div className="popup">
            <div className="popup_back" onClick={ ()=>{handlerPopUp(false)} } />
            <div className={`popup_cont bg-${ theme }`}>
                { children }
            </div>
        </div>
    );
};

export default Popup;
