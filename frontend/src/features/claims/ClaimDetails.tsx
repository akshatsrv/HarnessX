'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { Claim, ClaimDocument } from '../../types/claim';
import { RiskAssessment } from '../../types/risk';
import { fetchClaimDetails, assessRisk } from '../../services/api';
import { 
  ArrowLeft, FileText, AlertTriangle, ShieldAlert, Sparkles, CheckCircle2, 
  Car, Calendar, MapPin, Layers 
} from 'lucide-react';

export const ClaimDetails: React.FC = () => {
  const params = useParams();
  const id = params?.id as string | undefined;
  const router = useRouter();

  const [claim, setClaim] = useState<Claim | null>(null);
  const [documents, setDocuments] = useState<ClaimDocument[]>([]);
  const [risk, setRisk] = useState<RiskAssessment | null>(null);
  const [loading, setLoading] = useState(true);
  const [evaluating, setEvaluating] = useState(false);

  useEffect(() => {
    if (!id) return;
    fetchClaimDetails(id)
      .then((data) => {
        setClaim(data.claim);
        setDocuments(data.documents);
        setRisk(data.latest_risk || null);
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, [id]);

  const handleComputeRisk = async () => {
    if (!id) return;
    setEvaluating(true);
    try {
      const assessment = await assessRisk(id);
      setRisk(assessment);
    } catch (err) {
      console.error(err);
    } finally {
      setEvaluating(false);
    }
  };

  if (loading) {
    return <div style={{ padding: '60px', textAlign: 'center', color: 'var(--text-muted)' }}>Loading claim details...</div>;
  }

  if (!claim) {
    return <div style={{ padding: '60px', textAlign: 'center', color: 'var(--text-muted)' }}>Claim not found.</div>;
  }

  return (
    <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '32px 24px' }}>
      {/* Top Bar with Back Link */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
        <Link href="/" style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
          <ArrowLeft size={16} /> Back to Claims Queue
        </Link>
        <div style={{ display: 'flex', gap: '12px' }}>
          <button 
            onClick={handleComputeRisk} 
            disabled={evaluating} 
            className="btn-secondary"
          >
            {evaluating ? 'Recalculating Rules...' : 'Re-run Deterministic Rules'}
          </button>
          <button 
            onClick={() => router.push(`/investigations/${claim.claim_id}`)} 
            className="btn-primary"
            style={{ boxShadow: '0 0 20px rgba(59, 130, 246, 0.45)' }}
          >
            <Sparkles size={16} /> Investigate with AI
          </button>
        </div>
      </div>

      {/* Main Claim Header */}
      <div className="glass-panel" style={{ padding: '28px 32px', marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
              <h1 style={{ fontSize: '1.85rem', fontWeight: 800, fontFamily: 'var(--font-mono)' }}>
                {claim.claim_id}
              </h1>
              <span className="badge badge-high" style={{ fontSize: '0.85rem' }}>
                <AlertTriangle size={13} /> Flagged for Investigation
              </span>
            </div>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>
              Insured: <strong style={{ color: 'var(--text-main)' }}>Rajesh Kumar</strong> (Customer ID: {claim.customer_id}) • Vehicle: <strong style={{ color: 'var(--text-main)' }}>Honda City (V-301)</strong>
            </p>
          </div>

          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Claimed Amount
            </div>
            <div style={{ fontSize: '2.2rem', fontWeight: 800, color: '#f8fafc' }}>
              ₹{claim.claimed_amount.toLocaleString('en-IN')}
            </div>
          </div>
        </div>

        {/* Claim Meta Chips */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '16px',
          marginTop: '24px',
          paddingTop: '20px',
          borderTop: '1px solid var(--border-subtle)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Calendar size={18} color="#3b82f6" />
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Incident Date</div>
              <div style={{ fontSize: '0.9rem', fontWeight: 600 }}>{claim.incident_date}</div>
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <MapPin size={18} color="#3b82f6" />
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Incident Location</div>
              <div style={{ fontSize: '0.9rem', fontWeight: 600 }}>{claim.incident_location || 'Delhi'}</div>
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Car size={18} color="#3b82f6" />
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Reported Damage</div>
              <div style={{ fontSize: '0.9rem', fontWeight: 600 }}>{claim.damage_reported || 'Front collision'}</div>
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Layers size={18} color="#3b82f6" />
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Attached Documents</div>
              <div style={{ fontSize: '0.9rem', fontWeight: 600 }}>{documents.length} verified files</div>
            </div>
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 0.8fr', gap: '24px' }}>
        {/* Left Column: Documents & Extraction Discrepancy Highlight */}
        <div>
          {/* Discrepancy Alert Box */}
          <div style={{
            background: 'rgba(244, 63, 94, 0.12)',
            border: '1px solid rgba(244, 63, 94, 0.35)',
            borderRadius: '12px',
            padding: '20px',
            marginBottom: '24px'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
              <ShieldAlert size={20} color="#f43f5e" />
              <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#fda4af' }}>
                Document AI Temporal Discrepancy Detected
              </h3>
            </div>
            <p style={{ fontSize: '0.875rem', color: '#fecdd3', lineHeight: '1.5' }}>
              Cross-document field normalization identified conflicting accident dates:
              <br />
              • <strong>Claim Form (DOC-101):</strong> Incident Date: <strong>12 September 2026</strong>
              <br />
              • <strong>Police FIR (DOC-102):</strong> Occurrence Date: <strong>14 September 2026</strong>
              <br />
              <em>Under Policy Section 4.2, unexplained temporal variance &gt;24 hours requires manual investigator review.</em>
            </p>
          </div>

          {/* Documents Table */}
          <div className="glass-panel" style={{ padding: '24px', marginBottom: '24px' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '16px' }}>
              Submitted Claim Documents & Document AI Extractions
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {documents.map((doc) => (
                <div key={doc.document_id} style={{
                  background: 'rgba(255, 255, 255, 0.03)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '10px',
                  padding: '16px'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                      <FileText size={18} color="#60a5fa" />
                      <div>
                        <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>{doc.file_name}</div>
                        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>ID: {doc.document_id} • Type: {doc.document_type}</div>
                      </div>
                    </div>
                    <span className="badge badge-low">
                      <CheckCircle2 size={12} /> Extracted via DocAI
                    </span>
                  </div>

                  {/* Extracted fields snippet */}
                  <div style={{
                    background: 'rgba(0, 0, 0, 0.3)',
                    padding: '10px 12px',
                    borderRadius: '8px',
                    fontSize: '0.75rem',
                    fontFamily: 'var(--font-mono)',
                    color: '#94a3b8'
                  }}>
                    {JSON.stringify(doc.extracted_fields, null, 2)}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Explainable Risk Score & Signals */}
        <div>
          <div className="glass-panel" style={{ padding: '24px', position: 'sticky', top: '90px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>Deterministic Risk Engine</h3>
              <span className="badge badge-high">Rules v1</span>
            </div>

            {/* Score Ring / Bar */}
            <div style={{
              background: 'rgba(244, 63, 94, 0.08)',
              border: '1px solid rgba(244, 63, 94, 0.25)',
              borderRadius: '12px',
              padding: '20px',
              textAlign: 'center',
              marginBottom: '20px'
            }}>
              <div style={{ fontSize: '0.8rem', color: '#fda4af', fontWeight: 600, textTransform: 'uppercase' }}>
                Aggregate Risk Score
              </div>
              <div style={{ fontSize: '3rem', fontWeight: 800, color: '#f43f5e', margin: '4px 0' }}>
                {risk ? `${risk.score}/100` : '90/100'}
              </div>
              <div style={{ fontSize: '0.85rem', color: '#fecdd3' }}>
                Classification: <strong>HIGH RISK (ESCALATED)</strong>
              </div>
            </div>

            {/* Risk Signals List */}
            <div style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '12px' }}>
              Triggered Risk Indicators ({risk?.signals.length || 4}):
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '24px' }}>
              <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '12px', borderRadius: '8px', borderLeft: '3px solid #f43f5e' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>
                  <span>Document Date Mismatch</span>
                  <span style={{ color: '#f43f5e' }}>+15 pts</span>
                </div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  Accident date on claim form differs from police report.
                </div>
              </div>

              <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '12px', borderRadius: '8px', borderLeft: '3px solid #f43f5e' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>
                  <span>Repair Estimate Anomaly</span>
                  <span style={{ color: '#f43f5e' }}>+20 pts</span>
                </div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  Estimate (₹4,85,000) exceeds BigQuery baseline (₹2,10,000) by 130%.
                </div>
              </div>

              <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '12px', borderRadius: '8px', borderLeft: '3px solid #f59e0b' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>
                  <span>Repeat Claim Frequency</span>
                  <span style={{ color: '#f59e0b' }}>+20 pts</span>
                </div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  Customer has 3 prior claims (1 under review 4 months ago).
                </div>
              </div>

              <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '12px', borderRadius: '8px', borderLeft: '3px solid #3b82f6' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>
                  <span>Policy Inspection Trigger</span>
                  <span style={{ color: '#3b82f6' }}>+10 pts</span>
                </div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  Exceeds ₹2,50,000 policy threshold requiring physical survey.
                </div>
              </div>
            </div>

            {/* Launch AI CTA */}
            <button 
              onClick={() => router.push(`/investigations/${claim.claim_id}`)}
              className="btn-primary" 
              style={{ width: '100%', padding: '14px' }}
            >
              <Sparkles size={18} /> Launch Gemini Investigation
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
export default ClaimDetails;
