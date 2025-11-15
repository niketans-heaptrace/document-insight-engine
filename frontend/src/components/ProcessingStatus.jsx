import { useEffect, useState } from 'react';
import { documentAPI } from '../services/api';

const ProcessingStatus = ({ documentId, onProcessingComplete }) => {
  const [status, setStatus] = useState('processing');
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const doc = await documentAPI.getDocument(documentId);
        
        if (doc.status === 'completed') {
          setStatus('completed');
          setProgress(100);
          if (onProcessingComplete) {
            onProcessingComplete(doc);
          }
        } else if (doc.status === 'failed') {
          setStatus('failed');
        } else {
          // Update progress based on status
          const progressMap = {
            'uploaded': 20,
            'processing': 50,
            'extracting': 70,
            'analyzing': 90,
          };
          setProgress(progressMap[doc.status] || 30);
        }
      } catch (error) {
        console.error('Error checking status:', error);
      }
    };

    // Check status immediately
    checkStatus();

    // Poll every 2 seconds
    const interval = setInterval(checkStatus, 2000);

    return () => clearInterval(interval);
  }, [documentId, onProcessingComplete]);

  return (
    <div className="processing-status">
      <div className="status-header">
        <h2>Processing Document</h2>
        <div className={`status-badge status-${status}`}>
          {status === 'processing' && 'Processing...'}
          {status === 'completed' && 'Completed'}
          {status === 'failed' && 'Failed'}
        </div>
      </div>

      <div className="progress-container">
        <div className="progress-bar">
          <div
            className="progress-fill"
            style={{ width: `${progress}%` }}
          />
        </div>
        <p className="progress-text">{progress}%</p>
      </div>

      {status === 'processing' && (
        <div className="processing-steps">
          <div className="step active">
            <span className="step-icon">📄</span>
            <span>Uploading document</span>
          </div>
          <div className={`step ${progress > 20 ? 'active' : ''}`}>
            <span className="step-icon">🔍</span>
            <span>Extracting text</span>
          </div>
          <div className={`step ${progress > 50 ? 'active' : ''}`}>
            <span className="step-icon">🤖</span>
            <span>Analyzing with AI</span>
          </div>
          <div className={`step ${progress > 90 ? 'active' : ''}`}>
            <span className="step-icon">✨</span>
            <span>Generating insights</span>
          </div>
        </div>
      )}

      {status === 'failed' && (
        <div className="error-message">
          Processing failed. Please try uploading again.
        </div>
      )}
    </div>
  );
};

export default ProcessingStatus;

