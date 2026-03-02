import React, { useState, useEffect } from 'react';
import './NavBar.css';

export default function Navbar() {
  const [stickyClass, setStickyClass] = useState('');
  const [openMenu, setBurguerMenuOpen] = useState(false);

  useEffect(() => {
    window.addEventListener('scroll', stickNavbar);
    window.addEventListener("resize", hideMenuOnWideScreen);
  }, []);

  const stickNavbar = () => {
    if (window !== undefined) {
      let windowHeight = window.scrollY;
      // window height changed for the demo
      windowHeight > 62 ? setStickyClass('sticky-nav') : setStickyClass('');

    }
  };

  const hideMenuOnWideScreen = () => {
    if (window !== undefined) {
        let windowWidth = window.innerWidth;
        // window width changed
        windowWidth > 768 && setBurguerMenuOpen(false);
    }

  }



onresize = (event) => { }

  return <nav className={`navbar ${stickyClass}`}>
                <input type="checkbox" id="nav-check" checked = {openMenu}/>
            <div className="nav-header">
                <div className="nav-title">
                Logo
                </div>
            </div>
            <div className="nav-btn">
                <label for="nav-check">
                <span className='line'></span>
                <span className='line'></span>
                <span className='line'></span>
                </label>
            </div>

            <ul className="nav-list">
                <li><a href="#">Home</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Contact</a></li>
            </ul>
        </nav>;
}
