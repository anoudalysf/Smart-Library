import React, { useState } from 'react';
import './ChatModel.css';

const ChatBubble = ({ message, isUser }) => {
    return (
      <div className={`chat-bubble ${isUser ? 'user' : 'bot'}`}>
        <p><strong>{isUser ? 'User' : 'Bot'}:</strong> {message}</p>
      </div>
    );
  };

const ChatModel = ({ onClick, responses }) => {
  const [query, setQuery] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    if (query) {
      await onClick(query);
      setQuery('');
    }
  };

  return (
    <div className="chat-model">
      <div className="chat-history">
        {responses.map((msg, index) => (
            <ChatBubble
                key={index}
                message={msg.user || msg.bot}
                isUser={!!msg.user}
            />
            ))}
      </div>
      <form className="chat-input" onSubmit={handleSearch}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Type a message..."
        />
        <button type="submit">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <mask id="mask0_1_1891" style={{"mask-type":"luminance"}} maskUnits="userSpaceOnUse" x="2" y="3" width="20" height="20">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M2 3.00037H21.499V22.4994H2V3.00037Z" fill="white"/>
            </mask>
            <g mask="url(#mask0_1_1891)">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M10.8049 14.8178L14.4619 20.7508C14.6219 21.0108 14.8719 21.0078 14.9729 20.9938C15.0739 20.9798 15.3169 20.9178 15.4049 20.6228L19.9779 5.17777C20.0579 4.90477 19.9109 4.71877 19.8449 4.65277C19.7809 4.58677 19.5979 4.44577 19.3329 4.52077L3.87695 9.04677C3.58394 9.13277 3.51994 9.37877 3.50594 9.47977C3.49194 9.58277 3.48794 9.83777 3.74695 10.0008L9.74794 13.7538L15.0499 8.39577C15.3409 8.10177 15.8159 8.09877 16.1109 8.38977C16.4059 8.68077 16.4079 9.15677 16.1169 9.45077L10.8049 14.8178ZM14.8949 22.4998C14.1989 22.4998 13.5609 22.1458 13.1849 21.5378L9.30794 15.2468L2.95194 11.2718C2.26694 10.8428 1.90894 10.0788 2.01994 9.27577C2.12994 8.47277 2.68094 7.83477 3.45494 7.60777L18.9109 3.08177C19.6219 2.87377 20.3839 3.07077 20.9079 3.59277C21.4319 4.11977 21.6269 4.88977 21.4149 5.60377L16.8419 21.0478C16.6129 21.8248 15.9729 22.3738 15.1719 22.4808C15.0779 22.4928 14.9869 22.4998 14.8949 22.4998Z" fill="white"/>
            </g>
        </svg>
        </button>
      </form>
    </div>
  );
};

export default ChatModel;
