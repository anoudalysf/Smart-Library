import React, { useState } from "react";
import './AuthButton.css';
import AuthBox from '../AuthBox/AuthBox'
const AuthButton = () => {
    const [showAuthBox, setShowAuthBox] = useState(false);
    const [isOpen, setIsOpen] = useState(false);

    const toggleAuth = () => {
        setIsOpen(!isOpen);
        if (isOpen) {
            setShowAuthBox(false);
          }
      };
  
    const handleAuthClick = () => {
      setShowAuthBox(true);
      setIsOpen(false);
    };
  
    const handleCloseAuthBox = () => {
      setShowAuthBox(false);
    };
  
    return (
      <div>
        <button className="auth-toggle" onClick={toggleAuth}>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <mask id="mask0_85_9776" style={{"mask-type":"luminance"}} maskUnits="userSpaceOnUse" x="4" y="14" width="16" height="8">
          <path fill-rule="evenodd" clip-rule="evenodd" d="M4 14.4961H19.8399V21.8701H4V14.4961Z" fill="white"/>
      </mask>
      <g mask="url(#mask0_85_9776)">
          <path fill-rule="evenodd" clip-rule="evenodd" d="M11.921 15.9961C7.66 15.9961 5.5 16.7281 5.5 18.1731C5.5 19.6311 7.66 20.3701 11.921 20.3701C16.181 20.3701 18.34 19.6381 18.34 18.1931C18.34 16.7351 16.181 15.9961 11.921 15.9961ZM11.921 21.8701C9.962 21.8701 4 21.8701 4 18.1731C4 14.8771 8.521 14.4961 11.921 14.4961C13.88 14.4961 19.84 14.4961 19.84 18.1931C19.84 21.4891 15.32 21.8701 11.921 21.8701Z" fill="#41D0C8"/>
      </g>
      <mask id="mask1_85_9776" style={{"mask-type":"luminance"}} maskUnits="userSpaceOnUse" x="6" y="2" width="12" height="11">
          <path fill-rule="evenodd" clip-rule="evenodd" d="M6.60986 2.00012H17.2299V12.6187H6.60986V2.00012Z" fill="white"/>
      </mask>
      <g mask="url(#mask1_85_9776)">
          <path fill-rule="evenodd" clip-rule="evenodd" d="M11.9209 3.42769C9.77989 3.42769 8.03789 5.16869 8.03789 7.30969C8.03089 9.4437 9.75989 11.1837 11.8919 11.1917L11.9209 11.9057V11.1917C14.0609 11.1917 15.8019 9.44969 15.8019 7.30969C15.8019 5.16869 14.0609 3.42769 11.9209 3.42769ZM11.9209 12.6187H11.8889C8.9669 12.6097 6.59989 10.2267 6.60989 7.30669C6.60989 4.3817 8.99189 1.99969 11.9209 1.99969C14.8489 1.99969 17.2299 4.38169 17.2299 7.30969C17.2299 10.2377 14.8489 12.6187 11.9209 12.6187Z" fill="#41D0C8"/>
      </g>
  </svg>
        </button>
        {showAuthBox && <AuthBox onClose={handleCloseAuthBox} />}
        {isOpen && (
        <div className="auth-box">
          <button className="auth-login" onClick={handleAuthClick}>Login</button>
          <button className="auth-signup" onClick={handleAuthClick}>Signup</button>
        </div>
      )}
      </div>
    );
  };
  
  export default AuthButton;

 

