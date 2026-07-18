'use client';

import { useState, useRef } from 'react';
import { CheckSquare, Trash2, Plus, Check } from 'lucide-react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { actionItemsApi } from '@/lib/api';
import { ActionItem } from '@/types';
import toast from 'react-hot-toast';

interface ActionItemsPanelProps {
  meetingId: string;
}

export default function ActionItemsPanel({ meetingId }: ActionItemsPanelProps) {
  const queryClient = useQueryClient();
  const [newText, setNewText] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  const { data: items = [] } = useQuery({
    queryKey: ['action-items', meetingId],
    queryFn: () => actionItemsApi.list(meetingId),
  });

  const createMutation = useMutation({
    mutationFn: (text: string) =>
      actionItemsApi.create(meetingId, { text, priority: 'medium' }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['action-items', meetingId] });
      setNewText('');
      toast.success('Action item added');
    },
    onError: () => toast.error('Failed to add action item'),
  });

  const toggleMutation = useMutation({
    mutationFn: ({ id, completed }: { id: string; completed: boolean }) =>
      actionItemsApi.update(id, { completed }),
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: ['action-items', meetingId] }),
    onError: () => toast.error('Failed to update'),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => actionItemsApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['action-items', meetingId] });
      toast.success('Action item removed');
    },
    onError: () => toast.error('Failed to delete'),
  });

  const handleAdd = () => {
    const text = newText.trim();
    if (!text) return;
    createMutation.mutate(text);
  };

  const pending = items.filter((i) => !i.completed);
  const completed = items.filter((i) => i.completed);

  return (
    <div className="summary-section">
      <div className="summary-section-header" style={{ cursor: 'default' }}>
        <div className="summary-section-title">
          <CheckSquare size={14} style={{ color: 'var(--accent-light)' }} />
          Action Items
          {pending.length > 0 && (
            <span className="badge badge-yellow" style={{ marginLeft: '4px' }}>{pending.length}</span>
          )}
        </div>
      </div>

      <div className="summary-section-body">
        <div className="action-items-list">
          {items.length === 0 && (
            <p style={{ fontSize: '13px', color: 'var(--text-muted)', textAlign: 'center', padding: '8px 0' }}>
              No action items yet
            </p>
          )}

          {/* Pending */}
          {pending.map((item) => (
            <ActionItemRow
              key={item.id}
              item={item}
              onToggle={() => toggleMutation.mutate({ id: item.id, completed: !item.completed })}
              onDelete={() => deleteMutation.mutate(item.id)}
            />
          ))}

          {/* Completed */}
          {completed.length > 0 && (
            <>
              <div style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: 600, marginTop: '8px', marginBottom: '4px' }}>
                COMPLETED ({completed.length})
              </div>
              {completed.map((item) => (
                <ActionItemRow
                  key={item.id}
                  item={item}
                  onToggle={() => toggleMutation.mutate({ id: item.id, completed: !item.completed })}
                  onDelete={() => deleteMutation.mutate(item.id)}
                />
              ))}
            </>
          )}

          {/* Add new */}
          <div className="add-action-form">
            <Plus size={14} style={{ color: 'var(--text-muted)', flexShrink: 0 }} />
            <input
              ref={inputRef}
              className="add-action-input"
              type="text"
              placeholder="Add action item..."
              value={newText}
              onChange={(e) => setNewText(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleAdd()}
              aria-label="New action item text"
            />
            {newText && (
              <button
                className="btn btn-primary btn-sm"
                onClick={handleAdd}
                disabled={createMutation.isPending}
              >
                Add
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function ActionItemRow({
  item,
  onToggle,
  onDelete,
}: {
  item: ActionItem;
  onToggle: () => void;
  onDelete: () => void;
}) {
  return (
    <div className={`action-item ${item.completed ? 'completed' : ''}`}>
      <button
        className={`action-item-checkbox ${item.completed ? 'checked' : ''}`}
        onClick={onToggle}
        aria-label={item.completed ? 'Mark incomplete' : 'Mark complete'}
      >
        {item.completed && <Check size={11} />}
      </button>

      <div style={{ flex: 1, minWidth: 0 }}>
        <div className="action-item-text">{item.text}</div>
        {item.assignee && (
          <div className="action-item-meta">
            <span className="action-item-assignee">@ {item.assignee}</span>
            <div className={`priority-dot priority-${item.priority}`} title={`${item.priority} priority`} />
          </div>
        )}
      </div>

      <div className="action-item-actions">
        <button
          className="icon-btn btn-sm"
          onClick={onDelete}
          style={{ color: 'var(--danger)' }}
          aria-label="Delete action item"
        >
          <Trash2 size={12} />
        </button>
      </div>
    </div>
  );
}
