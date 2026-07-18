'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  BookOpen,
  Search,
  MessageSquare,
  Plug,
  Settings,
  ChevronDown,
  Zap,
  Users,
  BarChart2,
} from 'lucide-react';
import { getInitials } from '@/lib/utils';
import toast from 'react-hot-toast';

const NAV_ITEMS = [
  { href: '/meetings', icon: BookOpen, label: 'Notebook' },
  { href: '/search', icon: Search, label: 'Search' },
  { href: '/askfred', icon: MessageSquare, label: 'AskFred', badge: 'AI' },
];

const PLACEHOLDER_ITEMS = [
  { icon: Users, label: 'Channels' },
  { icon: Plug, label: 'Integrations' },
  { icon: BarChart2, label: 'Analytics' },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="sidebar">
      {/* Logo */}
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">
          <Zap size={18} color="#fff" fill="#fff" />
        </div>
        <span className="sidebar-logo-text">Fireflies</span>
      </div>

      {/* Navigation */}
      <nav className="sidebar-nav">
        <span className="sidebar-section-label">Workspace</span>

        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const isActive = pathname.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`sidebar-item ${isActive ? 'active' : ''}`}
            >
              <Icon size={16} className="sidebar-item-icon" />
              <span>{item.label}</span>
              {item.badge && (
                <span className="sidebar-badge">{item.badge}</span>
              )}
            </Link>
          );
        })}

        <span className="sidebar-section-label" style={{ marginTop: '8px' }}>
          More
        </span>

        {PLACEHOLDER_ITEMS.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.label}
              className="sidebar-item"
              onClick={() => toast(`${item.label} — Coming Soon`, { icon: '🚧' })}
            >
              <Icon size={16} className="sidebar-item-icon" />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="sidebar-footer">
        <Link href="/settings" className={`sidebar-item ${pathname === '/settings' ? 'active' : ''}`}>
          <Settings size={16} className="sidebar-item-icon" />
          <span>Settings</span>
        </Link>

        <div className="sidebar-user">
          <div
            className="avatar"
            style={{ backgroundColor: '#7C3AED' }}
          >
            {getInitials('Demo User')}
          </div>
          <div className="sidebar-user-info">
            <div className="sidebar-user-name">Demo User</div>
            <div className="sidebar-user-plan">Pro Plan</div>
          </div>
          <ChevronDown size={14} style={{ color: 'var(--text-muted)', flexShrink: 0 }} />
        </div>
      </div>
    </aside>
  );
}
