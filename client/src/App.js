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


import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import BillList from './pages/BillList';
import BillDetail from './pages/BillDetail';
import UserProfile from './pages/UserProfile';
import CreateBill from './pages/CreateBill';
import EditProfile from './pages/EditProfile';

const App = () => {
    return (
        <Router>
            <div className="App">
                <Header />
                <main>
                    <Switch>
                        <Route exact path="/" component={Home} />
                        <Route path="/login" component={Login} />
                        <Route path="/register" component={Register} />
                        <Route path="/bills" component={BillList} />
                        <Route path="/bill/:id" component={BillDetail} />
                        <Route path="/user/:id" component={UserProfile} />
                        <Route path="/create-bill" component={CreateBill} />
                        <Route path="/edit-profile" component={EditProfile} />
                        {/* Add other routes here */}
                    </Switch>
                </main>
                <Footer />
            </div>
        </Router>
    );
};

export default App;

