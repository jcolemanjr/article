import React,{useState} from "react";
import Bill from "./Bill";

function BillList({bills}) {

    const mappedBills = bills.map((bill) => {
        return (
            <Bill 
            // onClick={() => handleBillCLick(bill)}
            key={bill.id}
            title={bill.title}

            />
        )
    })

    return (
        <div>
          <h1 className="BillList">Bills</h1>
          {/* <Search setFilteredBills={setFilteredBills} /> */}
          <div className="mappedbill">{mappedBills}</div>
        </div>
      );
}

export default BillList;