import React from 'react';
import { Link } from 'react-router-dom'; // Import Link from react-router-dom

function Header() {
    return (
        <header className="App-header">
            <h1>Your App Name</h1>
            <nav>
                <ul>
                    <li><Link to="/">Home</Link></li>
                    <li><Link to="/BillList">Bill List</Link></li>
                    {/* Add more navigation links as needed */}
                </ul>
            </nav>
        </header>
    );
}

export default Header;
