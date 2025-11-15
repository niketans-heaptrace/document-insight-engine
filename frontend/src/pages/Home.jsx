import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import DocumentUpload from '../components/DocumentUpload';

const Home = () => {
  const navigate = useNavigate();
  const [recentDocuments, setRecentDocuments] = useState([]);

  const handleUploadSuccess = (result) => {
    // Navigate to document detail page
    navigate(`/documents/${result.id}`);
  };

  return (
    <div className="home-page">
      <header className="hero-section">
        <h1>Document Intelligence Platform</h1>
        <p className="subtitle">
          Upload any PDF, Word, or Image document and get AI-powered insights
        </p>
      </header>

      <main className="main-content">
        <section className="upload-section">
          <DocumentUpload onUploadSuccess={handleUploadSuccess} />
        </section>

        <section className="features-section">
          <h2>What You Can Do</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">📝</div>
              <h3>Auto-Summary</h3>
              <p>Generate concise summaries of your documents</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🔑</div>
              <h3>Key Points</h3>
              <p>Extract the most important points automatically</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h3>Table Extraction</h3>
              <p>Convert tables into structured, machine-readable data</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">💬</div>
              <h3>Q&A Chat</h3>
              <p>Ask questions and get answers about your documents</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🏷️</div>
              <h3>Classification</h3>
              <p>Detect sentiment and categorize documents</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🔍</div>
              <h3>Compare Documents</h3>
              <p>Compare multiple documents and find differences</p>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
};

export default Home;

