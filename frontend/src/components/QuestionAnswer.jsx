import { useState } from 'react';
import { documentAPI } from '../services/api';

const QuestionAnswer = ({ documentId }) => {
  const [question, setQuestion] = useState('');
  const [answers, setAnswers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await documentAPI.askQuestion(documentId, question);
      setAnswers([
        ...answers,
        {
          question,
          answer: response.answer,
          timestamp: new Date(),
        },
      ]);
      setQuestion('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to get answer');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="question-answer">
      <h3>💬 Ask Questions About This Document</h3>
      
      <form onSubmit={handleSubmit} className="qa-form">
        <div className="input-group">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask anything about the document..."
            className="question-input"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !question.trim()}
            className="ask-button"
          >
            {loading ? 'Asking...' : 'Ask'}
          </button>
        </div>
      </form>

      {error && <div className="error-message">{error}</div>}

      <div className="answers-container">
        {answers.length === 0 ? (
          <p className="no-answers">No questions asked yet. Start by asking a question above!</p>
        ) : (
          answers.map((qa, index) => (
            <div key={index} className="qa-item">
              <div className="question-bubble">
                <strong>Q:</strong> {qa.question}
              </div>
              <div className="answer-bubble">
                <strong>A:</strong> {qa.answer}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default QuestionAnswer;

