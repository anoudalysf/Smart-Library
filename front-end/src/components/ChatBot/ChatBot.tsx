import React, { useState } from 'react';
import ChatModel from '../ChatModel/ChatModel'; 
import styles from'./ChatBox.module.css';


interface ChatBotProp {
  onSend: (query: string) => Promise<string>;
}

interface Response {
  user?: string;
  bot?: string;
}

const ChatBot: React.FC<ChatBotProp> = ({ onSend }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [responses, setResponses] = useState<Response[]>([]); // for chat history

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const handleSend = async (query: string) => {
    setResponses(prevResponses => [...prevResponses, { user: query }]);
    let response = await onSend(query);
    response = response.replace(/\\n/g, '<br>');
    setResponses(prevResponses => [...prevResponses, { bot: response }]); //handle user and bot seperately (used to wait to send the query and response together)
  };

  return (
    <div>
      <button className={styles.chatToggle} onClick={toggleChat}>
      <svg width="45" height="45" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <mask id="mask0_1_1875" style={{"maskType":"luminance"}} maskUnits="userSpaceOnUse" x="1" y="1" width="22" height="22">
            <path fillRule="evenodd" clipRule="evenodd" d="M1 1.00024H22.493V22.494H1V1.00024Z" fill="white"/>
            </mask>
            <g mask="url(#mask0_1_1875)">
            <path fillRule="evenodd" clipRule="evenodd" d="M6.10844 19.6752C6.68844 19.6752 7.23544 19.8952 7.81444 20.1282C11.3614 21.7682 15.5564 21.0222 18.2894 18.2902C21.8954 14.6822 21.8954 8.81324 18.2894 5.20724C16.5434 3.46124 14.2214 2.50024 11.7494 2.50024C9.27644 2.50024 6.95344 3.46224 5.20844 5.20824C2.47444 7.94024 1.73044 12.1352 3.35544 15.6482C3.58944 16.2272 3.81544 16.7912 3.81544 17.3772C3.81544 17.9622 3.61444 18.5512 3.43744 19.0712C3.29144 19.4992 3.07044 20.1452 3.21244 20.2872C3.35144 20.4312 4.00144 20.2042 4.43044 20.0572C4.94544 19.8812 5.52944 19.6792 6.10844 19.6752ZM11.7244 22.4942C10.1964 22.4942 8.65844 22.1712 7.21944 21.5052C6.79544 21.3352 6.39844 21.1752 6.11344 21.1752C5.78544 21.1772 5.34444 21.3292 4.91844 21.4762C4.04444 21.7762 2.95644 22.1502 2.15144 21.3482C1.34944 20.5452 1.71944 19.4602 2.01744 18.5872C2.16444 18.1572 2.31544 17.7132 2.31544 17.3772C2.31544 17.1012 2.18244 16.7492 1.97844 16.2422C0.105437 12.1972 0.971437 7.32224 4.14844 4.14724C6.17644 2.11824 8.87544 1.00024 11.7484 1.00024C14.6214 1.00024 17.3214 2.11724 19.3494 4.14624C23.5414 8.33824 23.5414 15.1582 19.3494 19.3502C17.2944 21.4062 14.5274 22.4942 11.7244 22.4942Z" fill="white"/>
            </g>
            <path fillRule="evenodd" clipRule="evenodd" d="M15.6963 13.163C15.1443 13.163 14.6923 12.716 14.6923 12.163C14.6923 11.61 15.1353 11.163 15.6873 11.163H15.6963C16.2483 11.163 16.6963 11.61 16.6963 12.163C16.6963 12.716 16.2483 13.163 15.6963 13.163Z" fill="white"/>
            <path fillRule="evenodd" clipRule="evenodd" d="M11.6875 13.163C11.1355 13.163 10.6835 12.716 10.6835 12.163C10.6835 11.61 11.1255 11.163 11.6785 11.163H11.6875C12.2395 11.163 12.6875 11.61 12.6875 12.163C12.6875 12.716 12.2395 13.163 11.6875 13.163Z" fill="white"/>
            <path fillRule="evenodd" clipRule="evenodd" d="M7.67832 13.163C7.12632 13.163 6.67432 12.716 6.67432 12.163C6.67432 11.61 7.11732 11.163 7.66932 11.163H7.67832C8.23032 11.163 8.67832 11.61 8.67832 12.163C8.67832 12.716 8.23032 13.163 7.67832 13.163Z" fill="white"/>
        </svg>

      </button>
      {isOpen && (
                <div className={styles.chatBox}>
                <div className={styles.chatHeader}>
                  AI ChatBot
                </div>
                <ChatModel onClick={handleSend} responses={responses} />
              </div>
      )}
    </div>
  );
};

export default ChatBot;
