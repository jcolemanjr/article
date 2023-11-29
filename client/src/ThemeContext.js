// import React, { createContext, useState } from 'react';

// export const ThemeContext = createContext();

// export const ThemeProvider = ({ children }) => {
//     const [theme, setTheme] = useState('light'); // Default theme is light

//     const toggleTheme = () => {
//         setTheme(theme === 'light' ? 'dark' : 'light');
//     };

//     return (
//         <ThemeContext.Provider value={{ theme, toggleTheme }}>
//             {children}
//         </ThemeContext.Provider>
//     );
// };

// ThemeContext.js
import React, { createContext, useState, useContext } from 'react';

export const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
    const [theme, setTheme] = useState('light');
    const [user, setUser] = useState(null);

    const toggleTheme = () => {
        console.log("hello")
        setTheme(theme === 'light' ? 'dark' : 'light');
    };

    return (
        <ThemeContext.Provider value={{ theme, toggleTheme, user, setUser }}>
            {children}
        </ThemeContext.Provider>
    );
};

