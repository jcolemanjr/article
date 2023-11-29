import React,{useState, useContext} from "react";
import { ThemeContext } from './ThemeContext';
import Bill from "./Bill";

function BillList({bills}) {
    const {theme} = useContext(ThemeContext)
    const mappedBills = bills.map((bill) => {

        return (
            <Bill 
            key={bill.id}
            title={bill.title}
            id={bill.id}
            />
        )
    })

    return (
        <div className={`${theme}-theme`}>
          <h1 className="BillList">Bills</h1>
          {/* <Search setFilteredBills={setFilteredBills} /> */}
          <div className="mappedbill">{mappedBills}</div>
        </div>
      );
}

export default BillList;

// import React from 'react';
// import { Link } from 'react-router-dom';

// function BillList({ bills }) {
//   return (
//     <div>
//       <h1 className="BillList">Bills</h1>
//       <div className="mappedbill">
//         {bills.map((bill) => (
//           <div key={bill.id}>
//             {/* Wrap the bill title in a Link component */}
//             <Link to={`/bills/${bill.id}`}>{bill.title}</Link>
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// }

// export default BillList;
