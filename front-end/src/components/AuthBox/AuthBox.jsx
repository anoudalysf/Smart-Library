import React, { useState } from 'react';
import './AuthBox.css';

const AuthBox = ({ onClose, setAuth }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLogin, setIsLogin] = useState(true); //toggle between login and register

  const handleSubmit = async (event) => {
    event.preventDefault();
    const url = isLogin ? 'http://localhost:8000/users/login' : 'http://localhost:8000/users/register';

    let options;
    if (isLogin) {
      const data = new URLSearchParams();
      data.append('username', username);
      data.append('password', password);
      options = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: data.toString(),
      };
    } else {
      const data = { user_name: username, password: password };
      options = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      };
    }

    try {
      const response = await fetch(url, options);
      const result = await response.json();
      if (response.ok) {
        alert('Success');
        if (isLogin) {
          console.log("Role from response:", result.role);
          // save the token and username to localStorage
          localStorage.setItem('token', result.access_token);
          localStorage.setItem('username', username);
          localStorage.setItem('role', result.role);
          localStorage.setItem('user_id', result.user_id);
          setAuth(username, result.user_id, result.role);
        }
        // handle successful login/registration
        onClose();
      } else {
        alert(result.message || 'Incorrect Username or Password');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred. Please try again.');
    }
  };

  return (
    <div className="auth-box-container">
      <form onSubmit={handleSubmit} className="auth-box-form">
        <h2>{isLogin ? 'Log In' : 'Sign Up'} 
        <div style={{"height":"0.45px", "background-color": "#EAEFF5", "margin-top": "20px"}}></div>
        </h2>
        
        <label>
          Username:
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </label>
        <label>
          Password:
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
        <label2>
        <button type="submit">{isLogin ? 'Log In' : 'Sign Up'}</button>
        </label2>
        <label2>
        <button type="button" onClick={() => setIsLogin(!isLogin)}>
          {isLogin ? 'Switch to Sign Up' : 'Switch to Log In'}
        </button> </label2>
        <label2>
        <button type="button" onClick={onClose} className="close-button">Close</button> </label2>
      </form>
    </div>
  );
};

export default AuthBox;
