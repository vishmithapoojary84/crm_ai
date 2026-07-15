import React from 'react';

const Sidebar = () => {
  return (
    <aside className="sidebar">
      <h2>AI CRM</h2>
      <nav>
        <ul style={{ listStyle: 'none' }}>
          <li style={{ padding: '10px 0', cursor: 'pointer', color: 'var(--text-main)' }}>Dashboard</li>
          <li style={{ padding: '10px 0', cursor: 'pointer', color: 'var(--primary)' }}>Log Interaction</li>
          <li style={{ padding: '10px 0', cursor: 'pointer', color: 'var(--text-muted)' }}>HCP Database</li>
        </ul>
      </nav>
    </aside>
  );
};

export default Sidebar;
