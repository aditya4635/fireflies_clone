'use client';

import Sidebar from '@/components/layout/Sidebar';
import Topbar from '@/components/layout/Topbar';
import { Settings, User, Bell, Shield, Plug, Palette, Bot } from 'lucide-react';

const SETTING_SECTIONS = [
  {
    title: 'Account',
    icon: User,
    items: ['Profile & Name', 'Email Address', 'Password', 'Language & Region'],
  },
  {
    title: 'Notifications',
    icon: Bell,
    items: ['Email Notifications', 'Slack Notifications', 'Summary Ready Alerts', 'Action Item Reminders'],
  },
  {
    title: 'Integrations',
    icon: Plug,
    items: ['Google Calendar', 'Zoom', 'Google Meet', 'Microsoft Teams', 'Slack', 'Notion', 'HubSpot CRM'],
  },
  {
    title: 'AI & Bot',
    icon: Bot,
    items: ['Bot Name', 'Auto-join Meetings', 'Summary Language', 'Custom Vocabulary'],
  },
  {
    title: 'Privacy & Security',
    icon: Shield,
    items: ['Data Retention', 'Recording Consent', 'Two-Factor Auth', 'API Keys'],
  },
  {
    title: 'Appearance',
    icon: Palette,
    items: ['Theme (Dark / Light)', 'Transcript Font Size', 'Compact Mode'],
  },
];

export default function SettingsPage() {
  return (
    <div className="app-shell">
      <Sidebar />
      <div className="main-content">
        <Topbar />
        <main className="page-content">
          <div style={{ maxWidth: '760px' }}>
            <div className="dashboard-header" style={{ marginBottom: '32px' }}>
              <div>
                <h1 style={{ fontFamily: 'var(--font-heading)', fontSize: '22px', fontWeight: 700 }}>Settings</h1>
                <p style={{ color: 'var(--text-muted)', fontSize: '13px', marginTop: '4px' }}>
                  Manage your Fireflies workspace preferences
                </p>
              </div>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {SETTING_SECTIONS.map((section) => {
                const Icon = section.icon;
                return (
                  <div key={section.title} className="summary-section">
                    <div className="summary-section-header" style={{ cursor: 'default' }}>
                      <div className="summary-section-title">
                        <Icon size={14} style={{ color: 'var(--accent-light)' }} />
                        {section.title}
                      </div>
                      <span className="badge badge-gray" style={{ fontSize: '10px' }}>Coming Soon</span>
                    </div>
                    <div className="summary-section-body">
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                        {section.items.map((item) => (
                          <div
                            key={item}
                            style={{
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'space-between',
                              padding: '10px 14px',
                              background: 'var(--bg-elevated)',
                              borderRadius: 'var(--radius-sm)',
                              cursor: 'not-allowed',
                              opacity: 0.7,
                            }}
                          >
                            <span style={{ fontSize: '13.5px', color: 'var(--text-secondary)' }}>{item}</span>
                            <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>—</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
