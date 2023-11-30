import React, { useEffect, useState, useContext } from 'react';
import { ThemeContext } from './ThemeContext';
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

function BillDetail() {
    const {theme} = useContext(ThemeContext)
    const { user } = useContext(ThemeContext);
    const { billId } = useParams();
    const navigate = useNavigate();
    const [bill, setBill] = useState(null);

    useEffect(() => {
    // Fetch bill details from the server
        fetch(`http://localhost:5555/bill/${billId}`, {
          headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
      })
        .then((response) => response.json())
        .then((data) => setBill(data.bill))
        .catch((error) => console.error('Error fetching bill details:', error));
        }, [billId]);

    if (!bill) {
    return <div>Loading...</div>;
  }

    const handleEditClick = () => {
      navigate(`/edit-bill/${billId}`);
      };

    const handleDelete = async () => {
      const response = await fetch(`http://localhost:5555/bill/${billId}`, {
          method: 'DELETE',
          headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
      });

      if (response.ok) {
          // Handle successful deletion
          navigate('/BillList');
      } else {
          // Handle error in deletion
          console.error('Failed to delete bill');
      }
    }

    const handleVote = async (voteType) => {
      try {
          const response = await fetch('http://localhost:5555/vote', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${localStorage.getItem('token')}`
              },
              body: JSON.stringify({ bill_id: billId, vote_type: voteType })
          });

          if (response.ok) {
              console.log('Vote cast successfully');
          } else {
              console.error('Failed to cast vote');
          }
      } catch (error) {
          console.error('Error:', error);
      }
  };

  if (!bill) {
      return <div>Loading...</div>;
  }

  // className={`${theme}-theme`}
  return (
    <div className={`${theme}-theme`}>
      <h2>{bill.title}</h2>
      <p>Created by: {bill.uploaded_by}</p>
      <p>Summary: {bill.summary}</p>
      <p>Content: {bill.content}</p>
      <p>Vote Count: Yes: {bill.vote_count.Yes}, No: {bill.vote_count.No}, Abstain: {bill.vote_count.Abstain}</p>
      <button onClick={handleEditClick}>Edit</button>
      <button onClick={handleDelete}>Delete Bill</button>
      <button onClick={() => handleVote('Yes')}>Vote Yes</button>
      <button onClick={() => handleVote('No')}>Vote No</button>
      <button onClick={() => handleVote('Abstain')}>Abstain</button>
    </div>
  );
}

export default BillDetail;
