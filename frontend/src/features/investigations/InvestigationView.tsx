'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { InvestigationReport } from '../../types/investigation';
import { triggerInvestigation, createCase } from '../../services/api';
import { 
  ArrowLeft, Sparkles, CheckCircle2, ShieldCheck, AlertCircle, 
  BookOpen, Compass, ChevronRight, FileCheck2, Database 
} from 'lucide-react';

export const InvestigationView: React.FC = () => {
  const params = useParams();
  const id = params?.id as string | undefined;
  const router = useRouter();

  const [report, setReport] = useState<InvestigationReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [stepIndex, setStepIndex] = useState(0);
  const [creatingCase, setCreatingCase] = useState(false);

  const timelineSteps = [
    { label: 'Claim details retrieved', tool: 'get_claim_details' },
    { label: 'Previous claims queried from BigQuery', tool: 'get_customer_claim_history' },
    { label: 'Repair estimate compared against regional baseline', tool: 'get_repair_estimate_baseline' },
    { label: 'Extracted documents analyzed for discrepancies', tool: 'get_document_extraction' },
    { label: 'Insurance policy guidelines retrieved from Vertex AI Search', tool: 'search_insurance_policy' },
    { label: 'Gemini synthesized structured investigation report', tool: 'gemini-1.5-pro' },
  ];

  useEffect(() => {
    if (!id) return;

    // Simulate progressive tool execution visual steps
    const timer1 = setTimeout(() => setStepIndex(2), 600);
    const timer2 = setTimeout(() => setStepIndex(4), 1300);
    const timer3 = setTimeout(() => setStepIndex(6), 2000);

    triggerInvestigation(id)
      .then((data) => {
        setReport(data);
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));

    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
      clearTimeout(timer3);
    };
  }, [id]);

  const handleCreateCase = async () => {
    if (!report || !id) return;
    setCreatingCase(true);
    try {
      const newCase = await createCase(
        id,
        report.investigation_id,
        'Analyst review initiated based on Gemini AI findings: date discrepancy and repair estimate variance.'
      );
      router.push(`/cases/${newCase.case_id}`);
    } catch (err) {
      console.error(err);
    } finally {
      setCreatingCase(false);
    }
  };

  return (
    <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '32px 24px' }}>
      {/* Top Bar */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
        <Link href={`/claims/${id}`} style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
          <ArrowLeft size={16} /> Back to Claim {id}
        </Link>
        <span className="badge badge-info" style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <Sparkles size={12} /> Powered by Gemini on Vertex AI
        </span>
      </div>

      {/* Investigation Progress Timeline */}
      <div className="glass-panel" style={{ padding: '24px 32px', marginBottom: '32px' }}>
        <h2 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Database size={18} color="#3b82f6" /> Agent Tool Execution Trace
        </h2>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
          {timelineSteps.map((step, idx) => {
            const isDone = stepIndex > idx || !loading;
            return (
              <div 
                key={idx} 
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '12px',
                  padding: '12px 16px',
                  background: isDone ? 'rgba(16, 185, 129, 0.08)' : 'rgba(255, 255, 255, 0.02)',
                  border: `1px solid ${isDone ? 'rgba(16, 185, 129, 0.25)' : 'var(--border-subtle)'}`,
                  borderRadius: '10px',
                  transition: 'all 0.3s'
                }}
              >
                <div style={{ color: isDone ? '#10b981' : 'var(--text-faint)' }}>
                  {isDone ? <CheckCircle2 size={18} /> : <div style={{ width: '18px', height: '18px', borderRadius: '50%', border: '2px solid var(--text-faint)' }} />}
                </div>
                <div>
                  <div style={{ fontSize: '0.85rem', fontWeight: 600, color: isDone ? '#e2e8f0' : 'var(--text-muted)' }}>
                    {step.label}
                  </div>
                  <div style={{ fontSize: '0.7rem', color: 'var(--text-faint)', fontFamily: 'var(--font-mono)' }}>
                    {step.tool}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {loading && !report ? (
        <div style={{ padding: '80px', textAlign: 'center', color: 'var(--text-muted)' }}>
          <Sparkles size={32} style={{ animation: 'spin 2s linear infinite', marginBottom: '16px', color: '#60a5fa' }} />
          <div>Gemini is synthesizing evidence, querying BigQuery baselines, and evaluating policies...</div>
        </div>
      ) : report ? (
        <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 0.8fr', gap: '24px' }}>
          {/* Main Investigation Findings */}
          <div>
            {/* Assessment Banner */}
            <div className="glass-panel" style={{
              padding: '28px',
              marginBottom: '24px',
              borderLeft: '4px solid #f43f5e',
              background: 'linear-gradient(135deg, rgba(244, 63, 94, 0.1) 0%, rgba(15, 23, 42, 0.8) 100%)'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                <span className="badge badge-high">Assessment</span>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Investigation ID: {report.investigation_id}</span>
              </div>
              <h2 style={{ fontSize: '1.35rem', fontWeight: 700, color: '#ffffff', marginBottom: '12px' }}>
                {report.summary}
              </h2>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                Grounding Source: Synthesized from Document AI OCR extractions, BigQuery historical benchmarks, and IRDAI policy rules.
              </p>
            </div>

            {/* Findings List */}
            <div className="glass-panel" style={{ padding: '24px', marginBottom: '24px' }}>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <FileCheck2 size={18} color="#3b82f6" /> Evidence & Key Findings
              </h3>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
                {report.findings.map((f, idx) => (
                  <div key={idx} style={{
                    padding: '16px',
                    borderRadius: '10px',
                    background: 'rgba(255, 255, 255, 0.03)',
                    border: '1px solid var(--border-subtle)'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
                      <span style={{ fontWeight: 700, fontSize: '0.9rem', color: '#f1f5f9' }}>
                        {f.category}
                      </span>
                      <span className="badge badge-info" style={{ fontSize: '0.7rem' }}>
                        Confidence: {(f.confidence * 100).toFixed(0)}%
                      </span>
                    </div>
                    <p style={{ fontSize: '0.875rem', color: '#cbd5e1', lineHeight: '1.5', marginBottom: '10px' }}>
                      {f.description}
                    </p>
                    <div style={{ fontSize: '0.75rem', color: '#60a5fa', display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <strong>Evidence Source:</strong> {f.evidence_source}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Retrieved Policy References */}
            <div className="glass-panel" style={{ padding: '24px' }}>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <BookOpen size={18} color="#3b82f6" /> Retrieved Insurance Policy Clauses
              </h3>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
                {report.policy_references.map((p, idx) => (
                  <div key={idx} style={{
                    padding: '16px',
                    borderRadius: '10px',
                    background: 'rgba(59, 130, 246, 0.04)',
                    border: '1px solid rgba(59, 130, 246, 0.2)'
                  }}>
                    <div style={{ fontWeight: 700, fontSize: '0.9rem', color: '#93c5fd', marginBottom: '6px' }}>
                      {p.document_title} • {p.section}
                    </div>
                    <blockquote style={{
                      margin: '8px 0',
                      paddingLeft: '12px',
                      borderLeft: '2px solid #3b82f6',
                      color: '#e2e8f0',
                      fontSize: '0.85rem',
                      fontStyle: 'italic'
                    }}>
                      "{p.quote}"
                    </blockquote>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                      <strong>Relevance to Claim:</strong> {p.relevance}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Column: Recommendations, Uncertainties & Case CTA */}
          <div>
            <div className="glass-panel" style={{ padding: '24px', position: 'sticky', top: '90px' }}>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Compass size={18} color="#10b981" /> Recommended Next Actions
              </h3>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '24px' }}>
                {report.recommended_actions.map((act, idx) => (
                  <div key={idx} style={{
                    display: 'flex',
                    alignItems: 'flex-start',
                    gap: '10px',
                    padding: '12px',
                    borderRadius: '8px',
                    background: 'rgba(255, 255, 255, 0.03)',
                    border: '1px solid var(--border-subtle)',
                    fontSize: '0.85rem'
                  }}>
                    <ChevronRight size={16} color="#10b981" style={{ flexShrink: 0, marginTop: '2px' }} />
                    <span style={{ color: '#e2e8f0' }}>{act}</span>
                  </div>
                ))}
              </div>

              {/* Uncertainties Box */}
              <div style={{
                background: 'rgba(245, 158, 11, 0.08)',
                border: '1px solid rgba(245, 158, 11, 0.25)',
                borderRadius: '10px',
                padding: '16px',
                marginBottom: '24px'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px', color: '#fde68a', fontWeight: 600, fontSize: '0.85rem' }}>
                  <AlertCircle size={16} /> Known Uncertainties
                </div>
                <ul style={{ paddingLeft: '18px', fontSize: '0.8rem', color: '#cbd5e1', lineHeight: '1.5' }}>
                  {report.uncertainties.map((u, idx) => (
                    <li key={idx} style={{ marginBottom: '6px' }}>{u}</li>
                  ))}
                </ul>
              </div>

              {/* Create Case Button */}
              <button 
                onClick={handleCreateCase} 
                disabled={creatingCase}
                className="btn-primary" 
                style={{ width: '100%', padding: '14px' }}
              >
                <ShieldCheck size={18} /> 
                {creatingCase ? 'Creating Case in Firestore...' : 'Create Investigation Case'}
              </button>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
};
export default InvestigationView;
