'use client';

import { useRouter } from 'next/navigation';
import { Calendar, Clock, Trash2, Edit2, CheckSquare } from 'lucide-react';
import { Meeting } from '@/types';
import { formatDate, formatDuration, getInitials, truncate } from '@/lib/utils';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { meetingsApi } from '@/lib/api';
import toast from 'react-hot-toast';

interface MeetingCardProps {
  meeting: Meeting;
  onEdit: (meeting: Meeting) => void;
}

export default function MeetingCard({ meeting, onEdit }: MeetingCardProps) {
  const router = useRouter();
  const queryClient = useQueryClient();

  const deleteMutation = useMutation({
    mutationFn: () => meetingsApi.delete(meeting.id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['meetings'] });
      toast.success('Meeting deleted');
    },
    onError: () => toast.error('Failed to delete meeting'),
  });

  const handleDelete = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (confirm(`Delete "${meeting.title}"? This cannot be undone.`)) {
      deleteMutation.mutate();
    }
  };

  const handleEdit = (e: React.MouseEvent) => {
    e.stopPropagation();
    onEdit(meeting);
  };

  const displayParticipants = meeting.participants.slice(0, 4);
  const overflowCount = meeting.participants.length - 4;

  return (
    <article
      className="meeting-card"
      onClick={() => router.push(`/meetings/${meeting.id}`)}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === 'Enter' && router.push(`/meetings/${meeting.id}`)}
      aria-label={`Open meeting: ${meeting.title}`}
    >
      <div className="meeting-card-header">
        <h3 className="meeting-card-title">{meeting.title}</h3>
        <div className="meeting-card-actions">
          <button
            className="icon-btn btn-sm"
            onClick={handleEdit}
            title="Edit meeting"
            aria-label="Edit meeting"
          >
            <Edit2 size={14} />
          </button>
          <button
            className="icon-btn btn-sm"
            onClick={handleDelete}
            title="Delete meeting"
            aria-label="Delete meeting"
            style={{ color: 'var(--danger)' }}
          >
            <Trash2 size={14} />
          </button>
        </div>
      </div>

      <div className="meeting-card-meta">
        <span className="meeting-meta-item">
          <Calendar />
          {formatDate(meeting.date)}
        </span>
        <span className="meeting-meta-item">
          <Clock />
          {formatDuration(meeting.duration)}
        </span>
        <span className="meeting-meta-item">
          <CheckSquare />
          {meeting.participants.length} attendees
        </span>
      </div>

      <div className="meeting-card-footer">
        <div className="participants-row">
          {displayParticipants.map((p) => (
            <div
              key={p.id}
              className="avatar avatar-sm"
              style={{ backgroundColor: p.avatar_color }}
              title={p.name}
            >
              {getInitials(p.name)}
            </div>
          ))}
          {overflowCount > 0 && (
            <div className="participants-overflow">+{overflowCount}</div>
          )}
        </div>

        <span className="badge badge-purple">Processed</span>
      </div>
    </article>
  );
}
