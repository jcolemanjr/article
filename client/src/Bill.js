import React, {useEffect, useState} from "react";
import { useNavigate } from 'react-router-dom';



function Bill({onClick, title, id}) {
    const navigate = useNavigate();
    
    const handleBillClick = (billId) => {
    navigate(`/bills/${billId}`);
    };
    return (
        <div className="artwork">
          <h2 onClick={() => handleBillClick(id)} style={{ cursor: 'pointer' }}>{title}</h2>
          {/* <img
            onClick={() => {
              console.log("Works")
              onClick()
            }}
            src={image}
            alt={`This is a piece called ${descCheck()} by ${artistCheck()}`}
            title={`This is a piece called ${descCheck()} by ${artistCheck()}`}
          />
          <h3>Artist: {artistCheck()}</h3> */}
          {/* <p>Date: {date}</p>
          <p>Medium: {medium}</p>
          <p>Description: {descCheck()}</p>
          {isFavorite || isOnFavorites ? (
            <button
              className="removeButton"
              onClick={() => removeFromFavorites(id)}
            >
              <span>Remove From Favorites</span>
            </button>
          ) : (
            <button
              className="addButton"
              onClick={() =>
                addToFavorites({
                  title,
                  artist,
                  image,
                  date,
                  medium,
                  description,
                  accessionNumber,
                })
              }
            >
              <span>Add to Favorites</span>
            </button>
          )} */}
        </div>
      );
}

export default Bill;