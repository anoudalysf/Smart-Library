import React, { useState } from "react";
import RateIcon from "../RateIcon/RateIcon";
import "./BookCard.css"

const LikeIcon = () => {
  return(
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <mask id="mask0_1_1877" style={{"mask-type":"luminance"}} maskUnits="userSpaceOnUse" x="2" y="2" width="21" height="21">
      <path fill-rule="evenodd" clip-rule="evenodd" d="M2 2.99988H22.4725V22.5009H2V2.99988Z" fill="white"/>
      </mask>
      <g mask="url(#mask0_1_1877)">
      <path fill-rule="evenodd" clip-rule="evenodd" d="M3.82371 12.123C5.22571 16.485 10.7647 20.012 12.2367 20.885C13.7137 20.003 19.2927 16.437 20.6497 12.127C21.5407 9.341 20.7137 5.812 17.4277 4.753C15.8357 4.242 13.9787 4.553 12.6967 5.545C12.4287 5.751 12.0567 5.755 11.7867 5.551C10.4287 4.53 8.65471 4.231 7.03771 4.753C3.75671 5.811 2.93271 9.34 3.82371 12.123ZM12.2377 22.501C12.1137 22.501 11.9907 22.471 11.8787 22.41C11.5657 22.239 4.19271 18.175 2.39571 12.581C2.39471 12.581 2.39471 12.58 2.39471 12.58C1.26671 9.058 2.52271 4.632 6.57771 3.325C8.48171 2.709 10.5567 2.98 12.2347 4.039C13.8607 3.011 16.0207 2.727 17.8867 3.325C21.9457 4.634 23.2057 9.059 22.0787 12.58C20.3397 18.11 12.9127 22.235 12.5977 22.408C12.4857 22.47 12.3617 22.501 12.2377 22.501Z" fill="black"/>
      </g>
      <path fill-rule="evenodd" clip-rule="evenodd" d="M18.1537 10.6249C17.7667 10.6249 17.4387 10.3279 17.4067 9.9359C17.3407 9.1139 16.7907 8.4199 16.0077 8.1669C15.6127 8.0389 15.3967 7.6159 15.5237 7.2229C15.6527 6.8289 16.0717 6.6149 16.4677 6.7389C17.8307 7.1799 18.7857 8.3869 18.9027 9.8139C18.9357 10.2269 18.6287 10.5889 18.2157 10.6219C18.1947 10.6239 18.1747 10.6249 18.1537 10.6249Z" fill="black"/>
    </svg>

  )
}

// const RateIcon = () => {
//   return(
//     <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
//     <path fill-rule="evenodd" clip-rule="evenodd" d="M11.7499 4.5C11.6589 4.5 11.4349 4.525 11.3159 4.763L9.48992 8.414C9.20092 8.991 8.64392 9.392 7.99992 9.484L3.91192 10.073C3.64192 10.112 3.54992 10.312 3.52192 10.396C3.49692 10.477 3.45692 10.683 3.64292 10.861L6.59892 13.701C7.06992 14.154 7.28392 14.807 7.17192 15.446L6.47592 19.456C6.43292 19.707 6.58992 19.853 6.65992 19.903C6.73392 19.959 6.93192 20.07 7.17692 19.942L10.8319 18.047C11.4079 17.75 12.0939 17.75 12.6679 18.047L16.3219 19.941C16.5679 20.068 16.7659 19.957 16.8409 19.903C16.9109 19.853 17.0679 19.707 17.0249 19.456L16.3269 15.446C16.2149 14.807 16.4289 14.154 16.8999 13.701L19.8559 10.861C20.0429 10.683 20.0029 10.476 19.9769 10.396C19.9499 10.312 19.8579 10.112 19.5879 10.073L15.4999 9.484C14.8569 9.392 14.2999 8.991 14.0109 8.413L12.1829 4.763C12.0649 4.525 11.8409 4.5 11.7499 4.5ZM6.94692 21.5C6.53392 21.5 6.12392 21.37 5.77292 21.114C5.16692 20.67 4.86992 19.937 4.99892 19.199L5.69492 15.189C5.72092 15.04 5.66992 14.889 5.55992 14.783L2.60392 11.943C2.05992 11.422 1.86492 10.652 2.09492 9.937C2.32692 9.214 2.94092 8.697 3.69792 8.589L7.78592 8C7.94392 7.978 8.07992 7.881 8.14792 7.743L9.97492 4.091C10.3119 3.418 10.9919 3 11.7499 3C12.5079 3 13.1879 3.418 13.5249 4.091L15.3529 7.742C15.4219 7.881 15.5569 7.978 15.7139 8L19.8019 8.589C20.5589 8.697 21.1729 9.214 21.4049 9.937C21.6349 10.652 21.4389 11.422 20.8949 11.943L17.9389 14.783C17.8289 14.889 17.7789 15.04 17.8049 15.188L18.5019 19.199C18.6299 19.938 18.3329 20.671 17.7259 21.114C17.1109 21.565 16.3099 21.626 15.6309 21.272L11.9779 19.379C11.8349 19.305 11.6639 19.305 11.5209 19.379L7.86792 21.273C7.57592 21.425 7.26092 21.5 6.94692 21.5Z" fill="black"/>
//     </svg>
//   )
// }

const BookFront = ({ book }) => {
  return (
    // <div className="cover-photo">
      <img src={book.thumbnail} alt={book.title} />
    // </div>
  );
};

const BookBack = ({ book }) => {
  return (
      <h2 className="book-description">{book.description}</h2>
  );
};

const BookCard = ({ book }) => {
  const [isFlipped, setFlipped] = useState(false);

  const handleFlip = () => {
    setFlipped(!isFlipped);
  };

  return (
    <div className="book-item">
      <h2 className="book-title">{book.title}</h2>
      <div className="multiple-titles">
        <p className="book-sub-title">{book.authors}</p>
        <p className="book-sub-title">{book.published_year}</p>
      </div>
      <div className="cover-photo">
        <div className={`flip-card ${isFlipped ? "flipped" : ""}`} onClick={handleFlip}>
          <div className="flip-card-inner">
            <div className="flip-card-front">
              <BookFront book={book} />
            </div>
            <div className="flip-card-back">
              <BookBack book={book} />
              </div>
            </div>
          </div>
      </div>
      <div className="multiple-titles">
      <p className="book-sub-title">{book.categories}</p>
      <div className="book-rating">
      <p className="book-sub-title">{book.average_rating}
          <RateIcon rating={book.average_rating} /> </p>
        </div>
      </div>
    </div>
  );
};

export default BookCard;
