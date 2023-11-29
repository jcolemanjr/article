import React, {useContext} from 'react';

import { ThemeContext } from './ThemeContext';
import { Link } from 'react-router-dom'; // Import Link from react-router-dom

function Header() {
    const { toggleTheme } = useContext(ThemeContext);

    return (
        <header className="App-header">
            <h1>ArtIcle</h1>
            <nav>
                <ul>
                    <li><Link to="/">Home</Link></li>
                    <li><Link to="/BillList">Bill List</Link></li>
                    <li><Link to="/create-bill">Create Bill</Link></li>
                    <button onClick={toggleTheme}>Toggle Theme</button>
                    {/* Add more navigation links as needed */}
                </ul>
            </nav>
        </header>
    );
}

export default Header;
