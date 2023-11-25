import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import BillList from './BillList';
import Home from './Home';
import Header from './Header';
import LoginForm from './LoginForm';
import BillDetail from './BillDetail';
import CreateBill from './CreateBill';
import EditBill from './EditBill';

// import Footer from './components/Footer';


// import Register from './Register';


// import UserProfile from './UserProfile';

// import EditProfile from './EditProfile';

function App() {
  console.log("Hello")
  const [bills,setBills]=useState([])
  const [user,setUser]=useState(null)
  
  const handleLogin = async (username, password) => {
    try {
      const base64Credentials = btoa(username + ':' + password);
      const response = await fetch('http://localhost:5555/login', {
        method: 'POST',
        mode: 'cors',
        headers: {
          // 'Content-Type': 'application/json',
          'Authorization': `Basic ${base64Credentials}`,
        },
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        throw new Error('Login failed');
      }

      const data = await response.json();
      const token = data.token;
      console.log(data.token)
      localStorage.setItem('token', token); // Store the token
      setUser({ username, token }); // Update user state
    } catch (error) {
      console.error('Login error:', error);
    }
  }

  useEffect(() => {
    fetch("/bill")
      .then((res) => res.json())
      .then((data) => setBills(data.bills));
  },[])


    return (
      <div className="App">
        {!user ? <LoginForm onLogin={handleLogin} /> : <div>Welcome {user.username}</div>}
        <Router>
                <Header />
                <main>
                    <Routes>
                        <Route exact path="/" element={<Home />} />
                        <Route path="/loginForm" element={<LoginForm />} />
                        {/* <Route path="/register" element={<Register />} /> */}
                        <Route exact path="/BillList" element={<BillList bills={bills} />}/>
                        <Route path="/bills/:billId" element={<BillDetail />} />
                        <Route path="/edit-bill/:billId" element={<EditBill />} />
                        {/* <Route path="/bill/:id" element={<BillDetail />} /> */}
                        {/* <Route path="/user/:id" element={<UserProfile />} />  */}
                        <Route path="/create-bill" element={<CreateBill setBills={setBills}/>} />
                        {/* <Route path="/edit-profile" element={<EditProfile />} /> */}
                        Add other routes here
                    </Routes>
                </main>
                {/* <Footer /> */}
            
        </Router>
      </div>
    );
};

export default App;
// {!user ? <LoginForm onLogin={handleLogin} /> : <div>Welcome {user.username}</div>}
// pass user as props