import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

function BillDetail() {
    const { billId } = useParams();
    const [bill, setBill] = useState(null);

    useEffect(() => {
    // Fetch bill details from the server
        fetch(`http://localhost:5555/bill/${billId}`)
        .then((response) => response.json())
        .then((data) => setBill(data.bill))
        .catch((error) => console.error('Error fetching bill details:', error));
        }, [billId]);

    if (!bill) {
    return <div>Loading...</div>;
  }
  return (
    <div>
      <h2>{bill.title}</h2>
      <p>Created by: {bill.uploaded_by}</p>
      <p>Summary: {bill.summary}</p>
      <p>Content: {bill.content}</p>
      <p>Vote Count: Yes: {bill.vote_count.Yes}, No: {bill.vote_count.No}, Abstain: {bill.vote_count.Abstain}</p>
    </div>
  );
}

export default BillDetail;
