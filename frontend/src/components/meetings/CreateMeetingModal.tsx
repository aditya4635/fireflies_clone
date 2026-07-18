'use client';

import { useState } from 'react';
import { X, Plus, Trash2, UserPlus } from 'lucide-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { meetingsApi } from '@/lib/api';
import { Meeting, MeetingCreate } from '@/types';
import toast from 'react-hot-toast';

interface CreateMeetingModalProps {
  onClose: () => void;
  editMeeting?: Meeting | null;
}

const AVATAR_COLORS = [
  '#7C3AED', '#059669', '#DC2626', '#D97706',
  '#2563EB', '#DB2777', '#0891B2', '#65A30D',
];

export default function CreateMeetingModal({ onClose, editMeeting }: CreateMeetingModalProps) {
  const isEdit = !!editMeeting;
  const queryClient = useQueryClient();

  const [title, setTitle] = useState(editMeeting?.title ?? '');
  const [date, setDate] = useState(
    editMeeting
      ? new Date(editMeeting.date).toISOString().slice(0, 16)
      : new Date().toISOString().slice(0, 16)
  );
  const [duration, setDuration] = useState(
    editMeeting ? Math.floor(editMeeting.duration / 60) : 30
  );
  const [participants, setParticipants] = useState<Array<{ name: string; email: string }>>(
    editMeeting?.participants.map((p) => ({ name: p.name, email: p.email ?? '' })) ?? [
      { name: '', email: '' },
    ]
  );
  const [transcriptText, setTranscriptText] = useState('');

  const createMutation = useMutation({
    mutationFn: (data: MeetingCreate) => meetingsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['meetings'] });
      toast.success('Meeting created!');
      onClose();
    },
    onError: () => toast.error('Failed to create meeting'),
  });

  const updateMutation = useMutation({
    mutationFn: (data: { id: string; payload: any }) =>
      meetingsApi.update(data.id, data.payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['meetings'] });
      queryClient.invalidateQueries({ queryKey: ['meeting', editMeeting?.id] });
      toast.success('Meeting updated!');
      onClose();
    },
    onError: () => toast.error('Failed to update meeting'),
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const validParticipants = participants.filter((p) => p.name.trim());

    if (isEdit) {
      updateMutation.mutate({
        id: editMeeting!.id,
        payload: {
          title,
          date: new Date(date).toISOString(),
          duration: duration * 60,
          participants: validParticipants.map((p, i) => ({
            name: p.name,
            email: p.email || undefined,
            avatar_color: AVATAR_COLORS[i % AVATAR_COLORS.length],
          })),
        },
      });
    } else {
      createMutation.mutate({
        title,
        date: new Date(date).toISOString(),
        duration: duration * 60,
        participants: validParticipants.map((p, i) => ({
          name: p.name,
          email: p.email || undefined,
          avatar_color: AVATAR_COLORS[i % AVATAR_COLORS.length],
        })),
        transcript_text: transcriptText || undefined,
      });
    }
  };

  const addParticipant = () =>
    setParticipants((prev) => [...prev, { name: '', email: '' }]);

  const removeParticipant = (index: number) =>
    setParticipants((prev) => prev.filter((_, i) => i !== index));

  const updateParticipant = (index: number, field: 'name' | 'email', value: string) => {
    setParticipants((prev) =>
      prev.map((p, i) => (i === index ? { ...p, [field]: value } : p))
    );
  };

  const isLoading = createMutation.isPending || updateMutation.isPending;

  return (
    <div className="modal-overlay" onClick={(e) => e.target === e.currentTarget && onClose()}>
      <div className="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
        <div className="modal-header">
          <h2 className="modal-title" id="modal-title">
            {isEdit ? 'Edit Meeting' : 'New Meeting'}
          </h2>
          <button className="icon-btn" onClick={onClose} aria-label="Close modal">
            <X size={18} />
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            <div className="form-group">
              <label className="form-label" htmlFor="meeting-title">
                Meeting Title *
              </label>
              <input
                id="meeting-title"
                className="form-input"
                type="text"
                placeholder="e.g. Q3 Product Roadmap Planning"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
              />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
              <div className="form-group">
                <label className="form-label" htmlFor="meeting-date">Date & Time</label>
                <input
                  id="meeting-date"
                  className="form-input"
                  type="datetime-local"
                  value={date}
                  onChange={(e) => setDate(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="meeting-duration">Duration (minutes)</label>
                <input
                  id="meeting-duration"
                  className="form-input"
                  type="number"
                  min="1"
                  max="480"
                  value={duration}
                  onChange={(e) => setDuration(Number(e.target.value))}
                  required
                />
              </div>
            </div>

            {/* Participants */}
            <div className="form-group">
              <label className="form-label">Participants</label>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {participants.map((p, index) => (
                  <div key={index} style={{ display: 'flex', gap: '8px' }}>
                    <input
                      className="form-input"
                      type="text"
                      placeholder="Full name"
                      value={p.name}
                      onChange={(e) => updateParticipant(index, 'name', e.target.value)}
                      style={{ flex: 2 }}
                    />
                    <input
                      className="form-input"
                      type="email"
                      placeholder="Email (optional)"
                      value={p.email}
                      onChange={(e) => updateParticipant(index, 'email', e.target.value)}
                      style={{ flex: 2 }}
                    />
                    {participants.length > 1 && (
                      <button
                        type="button"
                        className="btn btn-ghost btn-icon"
                        onClick={() => removeParticipant(index)}
                        aria-label="Remove participant"
                      >
                        <Trash2 size={14} />
                      </button>
                    )}
                  </div>
                ))}
                <button
                  type="button"
                  className="btn btn-ghost btn-sm"
                  onClick={addParticipant}
                  style={{ alignSelf: 'flex-start' }}
                >
                  <UserPlus size={14} />
                  Add Participant
                </button>
              </div>
            </div>

            {/* Transcript (only on create) */}
            {!isEdit && (
              <div className="form-group">
                <label className="form-label" htmlFor="transcript-text">
                  Paste Transcript (optional)
                </label>
                <textarea
                  id="transcript-text"
                  className="form-input form-textarea"
                  placeholder={'Speaker Name: What they said\nAnother Speaker: Their response...'}
                  value={transcriptText}
                  onChange={(e) => setTranscriptText(e.target.value)}
                  rows={5}
                />
              </div>
            )}
          </div>

          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={isLoading || !title.trim()}>
              {isLoading ? 'Saving...' : isEdit ? 'Save Changes' : 'Create Meeting'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
