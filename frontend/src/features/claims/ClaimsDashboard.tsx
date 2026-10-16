'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { Claim } from '../../types/claim';
import { fetchClaims } from '../../services/api';
import { ShieldAlert, AlertTriangle, CheckCircle2, Clock, ArrowRight, Sparkles, Filter } from 'lucide-react';

export const ClaimsDashboard: React.FC = () => {
  const [claims, setClaims] = useState<Claim[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchClaims()
      .then((data) => setClaims(data.claims))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  const stats = [
    { label: 'Total Active Claims', value: claims.length || 3, icon: Clock, color: '#3b82f6' },
    { label: 'Requires Investigation', value: 1, icon: AlertTriangle, color: '#f43f5e' },
    { label: 'Active Investigation Cases', value: 1, icon: ShieldAlert, color: '#f59e0b' },
    { label: 'Auto-Approved Claims', value: 1, icon: CheckCircle2, color: '#10b981' },
  ];

  return (
    <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '32px 24px' }}>
      {/* Top Banner / Pitch */}
      <div className="glass-panel" style={{
        padding: '24px 32px',
        marginBottom: '32px',
        background: 'linear-gradient(135deg, rgba(30, 41, 63, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%)',
        borderLeft: '4px solid #3b82f6',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
            <span className="badge badge-info"><Sparkles size={13} /> Decision Support Platform</span>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>BFSI Challenge Demonstration</span>
          </div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 800, marginBottom: '6px' }}>
            Claims Intake & Risk Investigation Center
          </h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', maxWidth: '720px' }}>
            Combines Google Document AI field extraction, deterministic risk engines, BigQuery historical baselines, and Gemini investigation reports to assist human investigators.
          </p>
        </div>

        <Link href="/claims/CLM-10291" className="btn-primary" style={{ padding: '12px 24px', whiteSpace: 'nowrap' }}>
          Open Demo Claim (CLM-10291)
          <ArrowRight size={16} />
        </Link>
      </div>

      {/* KPI Cards */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
        gap: '20px',
        marginBottom: '36px'
      }}>
        {stats.map((s, idx) => {
          const Icon = s.icon;
          return (
            <div key={idx} className="glass-panel" style={{ padding: '20px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
                <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 500 }}>
                  {s.label}
                </span>
                <div style={{
                  padding: '8px',
                  borderRadius: '8px',
                  background: `${s.color}15`,
                  color: s.color
                }}>
                  <Icon size={18} />
                </div>
              </div>
              <div style={{ fontSize: '2rem', fontWeight: 800, color: '#ffffff' }}>
                {s.value}
              </div>
            </div>
          );
        })}
      </div>

      {/* Claims Table Container */}
      <div className="glass-panel" style={{ overflow: 'hidden' }}>
        <div style={{
          padding: '20px 24px',
          borderBottom: '1px solid var(--border-subtle)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <div>
            <h2 style={{ fontSize: '1.15rem', fontWeight: 700 }}>Intake Claims Queue</h2>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              Synthetic motor claims with extracted document intelligence and risk indicators
            </p>
          </div>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button className="btn-secondary" style={{ padding: '8px 14px', fontSize: '0.8rem' }}>
              <Filter size={14} /> Filter Queue
            </button>
          </div>
        </div>

        {loading ? (
          <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
            Loading intake claims...
          </div>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.875rem' }}>
              <thead>
                <tr style={{ background: 'rgba(255, 255, 255, 0.02)', borderBottom: '1px solid var(--border-subtle)', color: 'var(--text-muted)' }}>
                  <th style={{ padding: '14px 20px', fontWeight: 600 }}>Claim ID</th>
                  <th style={{ padding: '14px 20px', fontWeight: 600 }}>Customer</th>
                  <th style={{ padding: '14px 20px', fontWeight: 600 }}>Incident Date</th>
                  <th style={{ padding: '14px 20px', fontWeight: 600 }}>Claimed Amount</th>
                  <th style={{ padding: '14px 20px', fontWeight: 600 }}>Reported Damage</th>
                  <th style={{ padding: '14px 20px', fontWeight: 600 }}>Status</th>
                  <th style={{ padding: '14px 20px', fontWeight: 600, textAlign: 'right' }}>Action</th>
                </tr>
              </thead>
              <tbody>
                {claims.map((claim) => {
                  const isHighRisk = claim.claim_id === 'CLM-10291';
                  return (
                    <tr
                      key={claim.claim_id}
                      style={{
                        borderBottom: '1px solid var(--border-subtle)',
                        background: isHighRisk ? 'rgba(244, 63, 94, 0.04)' : 'transparent',
                        transition: 'background 0.15s'
                      }}
                    >
                      <td style={{ padding: '16px 20px', fontWeight: 700, fontFamily: 'var(--font-mono)' }}>
                        <Link href={`/claims/${claim.claim_id}`} style={{ color: '#60a5fa', textDecoration: 'underline' }}>
                          {claim.claim_id}
                        </Link>
                      </td>
                      <td style={{ padding: '16px 20px', color: 'var(--text-main)', fontWeight: 500 }}>
                        {claim.customer_id}
                      </td>
                      <td style={{ padding: '16px 20px', color: 'var(--text-muted)' }}>
                        {claim.incident_date}
                      </td>
                      <td style={{ padding: '16px 20px', fontWeight: 700, color: '#f8fafc' }}>
                        ₹{claim.claimed_amount.toLocaleString('en-IN')}
                      </td>
                      <td style={{ padding: '16px 20px', color: 'var(--text-muted)' }}>
                        {claim.damage_reported || 'Collision damage'}
                      </td>
                      <td style={{ padding: '16px 20px' }}>
                        {isHighRisk ? (
                          <span className="badge badge-high">
                            <AlertTriangle size={12} /> High Risk (90/100)
                          </span>
                        ) : claim.status === 'APPROVED' ? (
                          <span className="badge badge-low">
                            <CheckCircle2 size={12} /> Low Risk (Auto)
                          </span>
                        ) : (
                          <span className="badge badge-medium">
                            <Clock size={12} /> Under Review
                          </span>
                        )}
                      </td>
                      <td style={{ padding: '16px 20px', textAlign: 'right' }}>
                        <Link
                          href={`/claims/${claim.claim_id}`}
                          className="btn-secondary"
                          style={{ padding: '6px 12px', fontSize: '0.8rem' }}
                        >
                          Review & Investigate <ArrowRight size={13} />
                        </Link>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
export default ClaimsDashboard;
