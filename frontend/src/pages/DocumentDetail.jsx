import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { documentAPI } from '../services/api';
import ProcessingStatus from '../components/ProcessingStatus';
import InsightsDisplay from '../components/InsightsDisplay';
import QuestionAnswer from '../components/QuestionAnswer';

const DocumentDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [document, setDocument] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDocument = async () => {
      try {
        const doc = await documentAPI.getDocument(id);
        setDocument(doc);
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to load document');
      } finally {
        setLoading(false);
      }
    };

    fetchDocument();
  }, [id]);

  const handleProcessingComplete = (doc) => {
    setDocument(doc);
  };

  if (loading) {
    return <div className="loading">Loading document...</div>;
  }

  if (error) {
    return (
      <div className="error-container">
        <p>{error}</p>
        <button onClick={() => navigate('/')}>Go Home</button>
      </div>
    );
  }

  if (!document) {
    return <div>Document not found</div>;
  }

  const isProcessing = document.status !== 'completed' && document.status !== 'failed';

  return (
    <div className="document-detail">
      <header className="document-header">
        <button onClick={() => navigate('/')} className="back-button">
          ← Back to Home
        </button>
        <h1>{document.filename}</h1>
        <div className="document-meta">
          <span>Uploaded: {new Date(document.uploaded_at).toLocaleString()}</span>
          <span className={`status-badge status-${document.status}`}>
            {document.status}
          </span>
        </div>
      </header>

      <main className="document-content">
        {isProcessing ? (
          <ProcessingStatus
            documentId={id}
            onProcessingComplete={handleProcessingComplete}
          />
        ) : (
          <>
            <InsightsDisplay document={document} />
            <QuestionAnswer documentId={id} />
          </>
        )}
      </main>
    </div>
  );
};

export default DocumentDetail;

