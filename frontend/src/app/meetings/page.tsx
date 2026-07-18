'use client';

import { useState, useCallback } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Search, BookOpen, SlidersHorizontal } from 'lucide-react';
import Sidebar from '@/components/layout/Sidebar';
import Topbar from '@/components/layout/Topbar';
import MeetingCard from '@/components/meetings/MeetingCard';
import CreateMeetingModal from '@/components/meetings/CreateMeetingModal';
import { meetingsApi } from '@/lib/api';
import { Meeting } from '@/types';
import { useDebounce } from '@/hooks/useDebounce';

export default function MeetingsPage() {
  const [searchInput, setSearchInput] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editMeeting, setEditMeeting] = useState<Meeting | null>(null);
  const [page, setPage] = useState(1);

  const debouncedSearch = useDebounce(searchInput, 300);

  const { data, isLoading, isError } = useQuery({
    queryKey: ['meetings', debouncedSearch, page],
    queryFn: () =>
      meetingsApi.list({ search: debouncedSearch || undefined, page, page_size: 20 }),
  });

  const handleEdit = useCallback((meeting: Meeting) => {
    setEditMeeting(meeting);
    setShowModal(true);
  }, []);

  const handleCloseModal = useCallback(() => {
    setShowModal(false);
    setEditMeeting(null);
  }, []);

  const handleNewMeeting = useCallback(() => {
    setEditMeeting(null);
    setShowModal(true);
  }, []);

  const meetings = data?.items ?? [];
  const total = data?.total ?? 0;

  return (
    <div className="app-shell">
      <Sidebar />
      <div className="main-content">
        <Topbar onNewMeeting={handleNewMeeting} />
        <main className="page-content">
          {/* Header */}
          <div className="dashboard-header">
            <div>
              <h1 className="dashboard-title">Notebook</h1>
              <p style={{ color: 'var(--text-muted)', fontSize: '13px', marginTop: '4px' }}>
                {total > 0 ? `${total} meeting${total !== 1 ? 's' : ''}` : 'Your meeting recordings and transcripts'}
              </p>
            </div>
            <button className="btn btn-primary" onClick={handleNewMeeting} id="create-meeting-btn">
              + New Meeting
            </button>
          </div>

          {/* Filter Bar */}
          <div className="filter-bar">
            <div className="search-wrapper">
              <Search size={14} className="search-wrapper-icon" />
              <input
                id="meeting-search"
                className="form-input"
                type="text"
                placeholder="Search meetings..."
                value={searchInput}
                onChange={(e) => {
                  setSearchInput(e.target.value);
                  setPage(1);
                }}
                aria-label="Search meetings"
              />
            </div>
            <button className="btn btn-secondary btn-sm">
              <SlidersHorizontal size={14} />
              Filters
            </button>
          </div>

          {/* Content */}
          {isLoading ? (
            <SkeletonGrid />
          ) : isError ? (
            <ErrorState onRetry={() => setPage(1)} />
          ) : meetings.length === 0 ? (
            <EmptyState
              hasSearch={!!debouncedSearch}
              onNewMeeting={handleNewMeeting}
            />
          ) : (
            <>
              <div className="meetings-grid">
                {meetings.map((meeting) => (
                  <MeetingCard
                    key={meeting.id}
                    meeting={meeting}
                    onEdit={handleEdit}
                  />
                ))}
              </div>

              {/* Pagination */}
              {total > 20 && (
                <div style={{ display: 'flex', justifyContent: 'center', gap: '8px', marginTop: '32px' }}>
                  <button
                    className="btn btn-secondary btn-sm"
                    disabled={page === 1}
                    onClick={() => setPage((p) => p - 1)}
                  >
                    Previous
                  </button>
                  <span style={{ display: 'flex', alignItems: 'center', color: 'var(--text-muted)', fontSize: '13px' }}>
                    Page {page} of {Math.ceil(total / 20)}
                  </span>
                  <button
                    className="btn btn-secondary btn-sm"
                    disabled={page * 20 >= total}
                    onClick={() => setPage((p) => p + 1)}
                  >
                    Next
                  </button>
                </div>
              )}
            </>
          )}
        </main>
      </div>

      {showModal && (
        <CreateMeetingModal
          onClose={handleCloseModal}
          editMeeting={editMeeting}
        />
      )}
    </div>
  );
}

function SkeletonGrid() {
  return (
    <div className="meetings-grid">
      {Array.from({ length: 6 }).map((_, i) => (
        <div key={i} className="card" style={{ height: '160px' }}>
          <div className="skeleton" style={{ height: '20px', width: '70%', marginBottom: '12px' }} />
          <div className="skeleton" style={{ height: '14px', width: '40%', marginBottom: '8px' }} />
          <div className="skeleton" style={{ height: '40px', marginTop: '8px' }} />
          <div className="skeleton" style={{ height: '26px', width: '30%', marginTop: '12px' }} />
        </div>
      ))}
    </div>
  );
}

function EmptyState({ hasSearch, onNewMeeting }: { hasSearch: boolean; onNewMeeting: () => void }) {
  return (
    <div className="empty-state">
      <div className="empty-state-icon">
        <BookOpen size={28} />
      </div>
      <h2 className="empty-state-title">
        {hasSearch ? 'No meetings found' : 'No meetings yet'}
      </h2>
      <p className="empty-state-desc">
        {hasSearch
          ? 'Try adjusting your search or clear the filters.'
          : 'Create your first meeting to get started. You can upload or paste a transcript.'}
      </p>
      {!hasSearch && (
        <button className="btn btn-primary" onClick={onNewMeeting}>
          + Create Your First Meeting
        </button>
      )}
    </div>
  );
}

function ErrorState({ onRetry }: { onRetry: () => void }) {
  return (
    <div className="empty-state">
      <div className="empty-state-icon" style={{ background: 'var(--danger-subtle)', color: 'var(--danger)' }}>
        <BookOpen size={28} />
      </div>
      <h2 className="empty-state-title">Failed to load meetings</h2>
      <p className="empty-state-desc">
        Make sure the backend is running at localhost:8000.
      </p>
      <button className="btn btn-primary" onClick={onRetry}>Retry</button>
    </div>
  );
}
