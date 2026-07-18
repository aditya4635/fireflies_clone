'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Search, Bell, Plus, HelpCircle } from 'lucide-react';

interface TopbarProps {
  onNewMeeting?: () => void;
}

export default function Topbar({ onNewMeeting }: TopbarProps) {
  const [query, setQuery] = useState('');
  const router = useRouter();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      router.push(`/search?q=${encodeURIComponent(query)}`);
    }
  };

  return (
    <header className="topbar">
      <form className="topbar-search" onSubmit={handleSearch}>
        <Search size={14} className="topbar-search-icon" />
        <input
          className="topbar-search-input"
          type="text"
          placeholder="Search meetings, transcripts..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </form>

      <div className="topbar-actions">
        <button
          className="btn btn-primary btn-sm"
          onClick={onNewMeeting}
          id="new-meeting-btn"
        >
          <Plus size={15} />
          New Meeting
        </button>

        <button className="icon-btn" title="Notifications" style={{ position: 'relative' }}>
          <Bell size={17} />
          <span className="notif-dot" />
        </button>

        <button className="icon-btn" title="Help">
          <HelpCircle size={17} />
        </button>
      </div>
    </header>
  );
}
