import React from 'react';

const Navbar = () => {
  return (
    <header className="navbar">
      <div className="user-profile" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <div style={{ width: '32px', height: '32px', borderRadius: '50%', backgroundColor: 'var(--primary)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold' }}>
          U
        </div>
        <span>User</span>
      </div>
    </header>
  );
};

export default Navbar;
