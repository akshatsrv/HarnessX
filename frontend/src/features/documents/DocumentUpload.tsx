'use client';

import React, { useState } from 'react';
import { UploadCloud, CheckCircle } from 'lucide-react';

interface DocumentUploadProps {
  claimId: string;
  onUploadSuccess?: () => void;
}

export const DocumentUpload: React.FC<DocumentUploadProps> = ({ claimId, onUploadSuccess }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [docType, setDocType] = useState('CLAIM_FORM');
  const [uploading, setUploading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) return;

    setUploading(true);
    try {
      // Step 1: Register document with backend API
      const res = await fetch(`/api/v1/claims/${claimId}/documents`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          file_name: selectedFile.name,
          document_type: docType,
          content_type: selectedFile.type || 'application/pdf'
        })
      });

      if (!res.ok) throw new Error('Failed to register document');
      const data = await res.json();

      // Step 2: Trigger Document AI extraction
      await fetch(`/api/v1/documents/${data.document_id}/extract`, { method: 'POST' });

      setSuccess(true);
      setSelectedFile(null);
      if (onUploadSuccess) onUploadSuccess();
    } catch (err) {
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="glass-panel" style={{ padding: '24px' }}>
      <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <UploadCloud size={18} color="#3b82f6" /> Upload Supporting Document
      </h3>

      <form onSubmit={handleUpload}>
        <div style={{ marginBottom: '14px' }}>
          <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '6px' }}>
            Document Classification
          </label>
          <select
            value={docType}
            onChange={(e) => setDocType(e.target.value)}
            style={{
              width: '100%',
              padding: '8px 12px',
              borderRadius: '8px',
              background: 'rgba(0,0,0,0.3)',
              border: '1px solid var(--border-subtle)',
              color: 'var(--text-main)',
              fontSize: '0.85rem'
            }}
          >
            <option value="CLAIM_FORM">Claim Form / Intimation</option>
            <option value="POLICE_REPORT">Police FIR / Incident Report</option>
            <option value="REPAIR_ESTIMATE">Workshop Repair Estimate</option>
            <option value="INSURANCE_POLICY">Policy Schedule / Endorsement</option>
          </select>
        </div>

        <div style={{ marginBottom: '16px' }}>
          <input
            type="file"
            accept=".pdf,.png,.jpg,.jpeg"
            onChange={(e) => {
              if (e.target.files && e.target.files[0]) {
                setSelectedFile(e.target.files[0]);
                setSuccess(false);
              }
            }}
            style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}
          />
        </div>

        <button
          type="submit"
          disabled={!selectedFile || uploading}
          className="btn-primary"
          style={{ width: '100%', padding: '10px' }}
        >
          {uploading ? 'Processing via Document AI...' : 'Upload & Extract Fields'}
        </button>

        {success && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#10b981', fontSize: '0.8rem', marginTop: '10px' }}>
            <CheckCircle size={14} /> Document registered and fields extracted successfully!
          </div>
        )}
      </form>
    </div>
  );
};
