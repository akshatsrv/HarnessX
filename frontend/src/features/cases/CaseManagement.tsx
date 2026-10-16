'use client';

import React, { useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { InvestigationCase, CaseStatus } from '../../types/case';
import { updateCaseStatus } from '../../services/api';
import { 
  ArrowLeft, FolderCheck, Clock, UserCheck, MessageSquarePlus, 
  Send, CheckCircle 
} from 'lucide-react';

export const CaseManagement: React.FC = () => {
  const params = useParams();
  const id = params?.id as string | undefined;

  // Demo case initial state fallback
  const [activeCase, setActiveCase] = useState<InvestigationCase>({
    case_id: id || 'CASE-10482',
    claim_id: 'CLM-10291',
    investigation_id: 'INV-DEMO-001',
    status: 'UNDER_INVESTIGATION',
    assigned_analyst_id: 'ANALYST-001',
    notes: [
      {
        note_id: 'NOTE-001',
        author_id: 'ANALYST-001',
        content: 'Case opened automatically following Gemini investigation. Flagged date discrepancy between claim form and FIR. Surveyor assigned to inspect vehicle at Apex Auto Care.',
        created_at: new Date().toISOString()
      }
    ],
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  });

  const [newNote, setNewNote] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const statuses: CaseStatus[] = [
    'OPEN',
    'UNDER_INVESTIGATION',
    'PENDING_INFORMATION',
    'APPROVED',
    'CLOSED'
  ];

  const handleStatusChange = async (newStatus: CaseStatus) => {
    setActiveCase((prev) => ({ ...prev, status: newStatus }));
    try {
      await updateCaseStatus(activeCase.case_id, newStatus);
    } catch (err) {
      console.error(err);
    }
  };

  const handleAddNote = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newNote.trim()) return;

    setSubmitting(true);
    try {
      const updated = await updateCaseStatus(activeCase.case_id, undefined, newNote);
      if (updated && updated.notes) {
        setActiveCase(updated);
      } else {
        setActiveCase((prev) => ({
          ...prev,
          notes: [
            ...prev.notes,
            {
              note_id: `NOTE-${Date.now()}`,
              author_id: 'ANALYST-001',
              content: newNote,
              created_at: new Date().toISOString()
            }
          ]
        }));
      }
      setNewNote('');
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '32px 24px' }}>
      {/* Top Bar */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
        <Link href={`/claims/${activeCase.claim_id}`} style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
          <ArrowLeft size={16} /> Return to Linked Claim ({activeCase.claim_id})
        </Link>
        <span className="badge badge-info">
          Firestore Persistent Case Record
        </span>
      </div>

      {/* Case Header Banner */}
      <div className="glass-panel" style={{ padding: '28px 32px', marginBottom: '28px' }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
              <h1 style={{ fontSize: '1.75rem', fontWeight: 800, fontFamily: 'var(--font-mono)' }}>
                {activeCase.case_id}
              </h1>
              <span className="badge badge-high" style={{ fontSize: '0.85rem' }}>
                <Clock size={13} /> {activeCase.status}
              </span>
            </div>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>
              Associated Claim: <Link href={`/claims/${activeCase.claim_id}`} style={{ color: '#60a5fa', fontWeight: 600 }}>{activeCase.claim_id}</Link> • Assigned Analyst: <strong style={{ color: 'var(--text-main)' }}>{activeCase.assigned_analyst_id}</strong>
            </p>
          </div>

          {/* Status Workflow Selector */}
          <div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Update Case Stage
            </div>
            <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
              {statuses.map((st) => {
                const isActive = activeCase.status === st;
                return (
                  <button
                    key={st}
                    onClick={() => handleStatusChange(st)}
                    style={{
                      padding: '6px 12px',
                      borderRadius: '8px',
                      fontSize: '0.75rem',
                      fontWeight: 600,
                      cursor: 'pointer',
                      border: isActive ? '1px solid #3b82f6' : '1px solid var(--border-subtle)',
                      background: isActive ? 'rgba(59, 130, 246, 0.25)' : 'rgba(255, 255, 255, 0.04)',
                      color: isActive ? '#ffffff' : 'var(--text-muted)',
                      transition: 'all 0.2s'
                    }}
                  >
                    {st}
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 0.8fr', gap: '24px' }}>
        {/* Left Column: Analyst Notes Log */}
        <div>
          <div className="glass-panel" style={{ padding: '24px', marginBottom: '24px' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <FolderCheck size={18} color="#3b82f6" /> Case Activity & Investigator Notes Log
            </h3>

            {/* Notes List */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginBottom: '24px' }}>
              {activeCase.notes.map((n, idx) => (
                <div key={idx} style={{
                  padding: '16px',
                  borderRadius: '10px',
                  background: 'rgba(255, 255, 255, 0.03)',
                  border: '1px solid var(--border-subtle)'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <UserCheck size={14} color="#60a5fa" />
                      <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#f1f5f9' }}>{n.author_id}</span>
                    </div>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-faint)' }}>
                      {new Date(n.created_at).toLocaleString()}
                    </span>
                  </div>
                  <p style={{ fontSize: '0.875rem', color: '#cbd5e1', lineHeight: '1.5' }}>
                    {n.content}
                  </p>
                </div>
              ))}
            </div>

            {/* Add Note Form */}
            <form onSubmit={handleAddNote} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)' }}>
                <MessageSquarePlus size={16} /> Add Investigator Note
              </div>
              <textarea
                value={newNote}
                onChange={(e) => setNewNote(e.target.value)}
                placeholder="Log physical survey observations, customer phone interview records, or SIU referral findings..."
                rows={3}
                style={{
                  width: '100%',
                  padding: '12px',
                  borderRadius: '8px',
                  background: 'rgba(0, 0, 0, 0.25)',
                  border: '1px solid var(--border-subtle)',
                  color: 'var(--text-main)',
                  fontFamily: 'var(--font-sans)',
                  fontSize: '0.875rem',
                  resize: 'vertical'
                }}
              />
              <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                <button 
                  type="submit" 
                  disabled={submitting || !newNote.trim()} 
                  className="btn-primary"
                  style={{ padding: '8px 18px', fontSize: '0.85rem' }}
                >
                  <Send size={14} /> {submitting ? 'Saving...' : 'Add Note to Case'}
                </button>
              </div>
            </form>
          </div>
        </div>

        {/* Right Column: Case Metadata & Evidence Summary */}
        <div>
          <div className="glass-panel" style={{ padding: '24px', position: 'sticky', top: '90px' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '16px' }}>
              Case Metadata
            </h3>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', fontSize: '0.85rem' }}>
              <div>
                <div style={{ color: 'var(--text-muted)', marginBottom: '4px' }}>Linked Investigation ID</div>
                <div style={{ fontFamily: 'var(--font-mono)', fontWeight: 600, color: '#93c5fd' }}>
                  {activeCase.investigation_id}
                </div>
              </div>

              <div>
                <div style={{ color: 'var(--text-muted)', marginBottom: '4px' }}>Assigned Special Unit</div>
                <div style={{ fontWeight: 600, color: '#f1f5f9' }}>
                  Motor Claims SIU - North Division
                </div>
              </div>

              <div>
                <div style={{ color: 'var(--text-muted)', marginBottom: '4px' }}>Mandatory Survey Requirement</div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#f43f5e', fontWeight: 600 }}>
                  <Clock size={14} /> On-site vehicle inspection pending
                </div>
              </div>

              <div style={{
                marginTop: '16px',
                paddingTop: '16px',
                borderTop: '1px solid var(--border-subtle)'
              }}>
                <button
                  onClick={() => handleStatusChange('APPROVED')}
                  className="btn-secondary"
                  style={{ width: '100%', marginBottom: '10px', borderColor: 'rgba(16, 185, 129, 0.4)', color: '#34d399' }}
                >
                  <CheckCircle size={16} /> Authorize & Clear Claim
                </button>
                <button
                  onClick={() => handleStatusChange('CLOSED')}
                  className="btn-secondary"
                  style={{ width: '100%', color: 'var(--text-muted)' }}
                >
                  Close Investigation File
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
export default CaseManagement;
