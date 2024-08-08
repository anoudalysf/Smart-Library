import React, { useState, ChangeEvent, FormEvent } from 'react';
import styles from './AuthBox.module.css';

const apiUrl = process.env.REACT_APP_API_URL as string;

interface AuthBoxProp{
  onClose: () => void;
  setAuth: (username: string, user_id: string, role: string) => void;
}

const AuthBox: React.FC<AuthBoxProp> = ({ onClose, setAuth }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLogin, setIsLogin] = useState(true); //toggle between login and register

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const url = isLogin ? `${apiUrl}/users/login` : `${apiUrl}/users/register`;

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
          //check if the user is still logged in
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
    <div className={styles.authBoxContainer}>
      <form onSubmit={handleSubmit} className={styles.authBoxForm}>
        <h2>{isLogin ? 'Log In' : 'Sign Up'} 
        <div style={{"height":"0.45px", "backgroundColor": "#EAEFF5", "marginTop": "20px"}}></div>
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
        <label>
        <button type="submit">{isLogin ? 'Log In' : 'Sign Up'}</button>
        </label>
        <label>
        <button type="button" onClick={() => setIsLogin(!isLogin)}>
          {isLogin ? 'Switch to Sign Up' : 'Switch to Log In'}
        </button></label>
        <label>
        <button type="button" onClick={onClose} className={styles.closeButton}>Close</button> </label>
      </form>
    </div>
  );
};

export default AuthBox;
