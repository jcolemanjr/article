import React, {useContext} from 'react';

import { ThemeContext } from './ThemeContext';
import { Link } from 'react-router-dom'; // Import Link from react-router-dom

function Header() {
    const { toggleTheme } = useContext(ThemeContext);

    return (
        <header className="App-header">
            <h1>ArtIcle</h1>
            <nav>
                <div>
                    <Link to="/">Home</Link>
                    <Link to="/BillList">Bill List</Link>
                    <Link to="/create-bill">Create Bill</Link>
                    <button onClick={toggleTheme}>Toggle Theme</button>
                    {/* Add more navigation links as needed */}
                </div>
            </nav>
        </header>
    );
}

export default Header;
