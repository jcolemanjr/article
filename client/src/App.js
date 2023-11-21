// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;


import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import BillList from './BillList';
import Home from './Home';
import Header from './Header';

// import Footer from './components/Footer';

// import Login from './pages/Login';
// import Register from './pages/Register';

// import BillDetail from './pages/BillDetail';
// import UserProfile from './pages/UserProfile';
// import CreateBill from './pages/CreateBill';
// import EditProfile from './pages/EditProfile';

function App() {
  console.log("Hello")
  const [bills,setBills]=useState([])
  const [user,setUser]=useState(null)

  useEffect(() => {
    fetch("/bill")
      .then((res) => res.json())
      .then((data) => setBills(data.bills));
  },[])


    return (
      <div className="App">
        <Router>
                <Header />
                <main>
                    <Routes>
                        <Route exact path="/" element={<Home />} />
                        {/* <Route path="/login" element={<Login />} /> */}
                        {/* <Route path="/register" element={<Register />} /> */}
                        <Route exact path="/BillList" element={<BillList bills={bills} />}/>
                        {/* <Route path="/bill/:id" element={<BillDetail />} />
                        <Route path="/user/:id" element={<UserProfile />} />
                        <Route path="/create-bill" element={<CreateBill />} />
                        <Route path="/edit-profile" element={<EditProfile />} /> */}
                        {/* Add other routes here */}
                    </Routes>
                </main>
                {/* <Footer /> */}
            
        </Router>
      </div>
    );
};

export default App;

