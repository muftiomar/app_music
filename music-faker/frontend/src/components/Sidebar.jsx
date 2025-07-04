import React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar = ({ toggleTheme }) => {
  const linkStyle = ({ isActive }) => ({
    padding: '1rem',
    display: 'block',
    textDecoration: 'none',
    color: isActive ? '#22c55e' : '#4b5563',
    fontWeight: isActive ? 'bold' : 'normal',
    backgroundColor: isActive ? '#1f2937' : 'transparent'
  });

  return (
    <div style={{
      width: '220px',
      background: 'var(--sidebar-bg)',
      paddingTop: '2rem',
      borderRight: '1px solid #1f2937',
      height: '100vh'
    }}>
      <h2 style={{ textAlign: 'center', color: '#22c55e' }}>🎵 Music</h2>
      <nav style={{ marginTop: '2rem' }}>
        <NavLink to="/" style={linkStyle}>🏠 Dashboard</NavLink>
        <NavLink to="/analytics" style={linkStyle}>📊 Analytics</NavLink>
      </nav>
      <div style={{ textAlign: 'center', marginTop: '2rem' }}>
        <button onClick={toggleTheme} style={{
          padding: '0.5rem 1rem',
          fontSize: '0.9rem',
          background: '#22c55e',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
          color: '#111827'
        }}>
          🌙 / ☀️ Thème
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
